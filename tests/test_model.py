import pathlib
import random

import pytest

torch = pytest.importorskip("torch")      # the network tests need torch; the rest of the suite does not

from alphafe.checker import Problem
from alphafe.env import start
from alphafe.model import (ModelConfig, NeuralProposer, PolicyValueNet, export_checkpoint, load_model, pad_batch,
                           save_checkpoint)
from alphafe.search import BestFirstSearch, run_searches
from alphafe.tokenizer import BOS, EOS, PAD, decode_move, encode_state

pytestmark = pytest.mark.usefixtures("plain_environment")      # see tests/conftest.py

TINY = ModelConfig(d_model=32, n_heads=2, enc_layers=1, dec_layers=1, d_ff=64)
CPU = torch.device("cpu")


def view_of(equation):
    state, _ = start(Problem.parse(equation))
    return encode_state(state)


def test_forward_shapes():
    model = PolicyValueNet(TINY)
    src = pad_batch([view_of("f(x+y) = f(x) + y").tokens, view_of("f(xy) = x*f(y)").tokens])
    tgt = torch.tensor([[BOS, 5, 6], [BOS, 7, PAD]])
    logits, value = model(src, tgt)
    assert logits.shape == (2, 3, TINY.vocab_size) and value.shape == (2,)
    assert torch.isfinite(logits).all() and torch.isfinite(value).all()


def test_default_model_size_is_in_the_planned_range():
    assert 1_000_000 <= PolicyValueNet().n_parameters() <= 5_000_000


def test_pad_batch_rounds_width_up():
    batch = pad_batch([[1, 2, 3], [4]], multiple=8)
    assert batch.shape == (2, 8) and batch[1, 1] == PAD


def test_proposals_are_well_formed_moves():
    torch.manual_seed(0)
    proposer = NeuralProposer(PolicyValueNet(TINY), CPU, n_uniform=2, rng=random.Random(0))
    views = [view_of("f(x+y) = f(x) + y"), view_of("f(x)f(y) = f(x+y) + xy"), view_of("f(xy) = x*f(y)")]
    proposals = proposer.propose(views, k=6)
    assert len(proposals) == 3
    for view, props in zip(views, proposals):
        assert 1 <= len(props) <= 6
        for ids, logp in props:
            assert ids[-1] == EOS and logp <= 0
            decode_move(ids, view)          # must not raise
    values = proposer.values(views)
    assert len(values) == 3 and all(0 <= v <= 1 for v in values)
    many = proposer.values(views * 7)                      # batches are padded internally; the answers are not
    assert len(many) == 21 and all(abs(a - b) < 1e-5 for a, b in zip(many[:3], values))


def test_untrained_network_can_drive_search():
    torch.manual_seed(0)
    proposer = NeuralProposer(PolicyValueNet(TINY), CPU)
    search = BestFirstSearch(Problem.parse("f(x+y) = f(x) + y"), budget=300)
    run_searches([search], proposer, k=8)
    assert search.done and search.calls <= 300


def test_checkpoint_round_trip(tmp_path):
    model = PolicyValueNet(TINY)
    path = tmp_path / "m.pt"
    save_checkpoint(path, model, {"note": "hello"})
    loaded, payload = load_model(path, CPU)
    assert payload["note"] == "hello" and loaded.config == TINY
    for a, b in zip(model.parameters(), loaded.parameters()):
        assert torch.equal(a, b)


def test_exported_checkpoint_keeps_the_weights_and_drops_the_training_state(tmp_path):
    torch.manual_seed(0)
    model = PolicyValueNet(TINY)
    optimizer = torch.optim.AdamW(model.parameters())
    full, slim = tmp_path / "full.pt", tmp_path / "slim.pt"
    save_checkpoint(full, model, {"optimizer": optimizer.state_dict(), "rng": random.Random(0).getstate(),
                                  "state": {"iteration": 3}, "train_config": {"run": "t"}})
    export_checkpoint(full, slim)
    raw = torch.load(slim, map_location="cpu", weights_only=True)
    # The export keeps what identifies the weights (vocabulary, commit, torch) and drops optimiser and random state.
    assert set(raw) == {"config", "model", "state", "train_config", "vocab", "commit", "torch"}
    loaded, payload = load_model(slim, CPU)
    assert payload["state"] == {"iteration": 3}
    for name, tensor in model.state_dict().items():
        assert torch.equal(tensor, loaded.state_dict()[name])


def test_loading_a_checkpoint_never_runs_code_from_the_file(tmp_path):
    # A pickle can ask for any function to be called on load. load_model must refuse.
    class Payload:
        def __reduce__(self):
            return (pathlib.Path.touch, (tmp_path / "ran",))

    path = tmp_path / "evil.pt"
    torch.save({"config": {}, "model": {}, "extra": Payload()}, path)
    with pytest.raises(Exception):
        load_model(path, CPU)
    assert not (tmp_path / "ran").exists()


def test_value_guided_search_with_network():
    torch.manual_seed(0)
    proposer = NeuralProposer(PolicyValueNet(TINY), CPU)
    search = BestFirstSearch(Problem.parse("f(x+y) = f(x) + y"), budget=120, value_weight=1.0)
    run_searches([search], proposer, k=8)
    assert search.done and search.calls <= 120 and len(search.nodes) > 1


def test_checkpoints_record_their_vocabulary_and_a_mismatch_is_refused(tmp_path, monkeypatch):
    """Token ids mean nothing without the vocabulary. A reordered vocabulary of the same size used to load
    without any error and score a little worse; now it is refused with the first differing token named."""
    from alphafe import tokenizer
    from alphafe.model import VocabularyMismatch

    path = tmp_path / "m.pt"
    save_checkpoint(path, PolicyValueNet(TINY), {})
    payload = torch.load(path, map_location="cpu", weights_only=True)
    assert payload["vocab"] == tokenizer.VOCAB and payload["torch"] == torch.__version__ and "commit" in payload
    load_model(path, CPU)                                              # the vocabulary it was saved with
    swapped = list(tokenizer.VOCAB)
    i, j = swapped.index("x"), swapped.index("y")
    swapped[i], swapped[j] = swapped[j], swapped[i]
    monkeypatch.setattr(tokenizer, "VOCAB", swapped)
    with pytest.raises(VocabularyMismatch, match=f"token {min(i, j)} is 'x' there and 'y' in the code now"):
        load_model(path, CPU)
    monkeypatch.setattr(tokenizer, "VOCAB", list(payload["vocab"]) + ["NEW"])
    with pytest.raises(VocabularyMismatch, match="'NEW' in the code now"):
        load_model(path, CPU)


def test_a_checkpoint_from_before_the_vocabulary_was_recorded_loads_only_if_the_size_matches(tmp_path, monkeypatch):
    from dataclasses import asdict

    from alphafe import tokenizer
    from alphafe.model import VocabularyMismatch

    path = tmp_path / "old.pt"
    model = PolicyValueNet(TINY)
    torch.save({"config": asdict(model.config), "model": model.state_dict()}, path)     # the v0.1.0 format
    load_model(path, CPU)
    monkeypatch.setattr(tokenizer, "VOCAB", list(tokenizer.VOCAB) + ["NEW"])
    with pytest.raises(VocabularyMismatch, match="tokens and the code now has"):
        load_model(path, CPU)


def test_solve_keeps_within_its_budget_and_repeats_with_a_seed():
    """The search stage used to get the whole budget after 32 calls had been spent without backtracking."""
    from alphafe.cli import _solve_with_network

    problem = Problem.parse("f(x)f(y) = f(x+y) + xy")
    outcomes = []
    for _ in range(2):
        torch.manual_seed(7)
        model = PolicyValueNet(TINY)
        torch.manual_seed(3)
        result = _solve_with_network(problem, model, CPU, budget=60, max_depth=16, seconds=60)
        assert result.checker_calls <= 60
        outcomes.append((result.solved, result.checker_calls))
    assert outcomes[0] == outcomes[1]                                   # same seed, same device: same run
    stopped = _solve_with_network(problem, PolicyValueNet(TINY), CPU, budget=5000, max_depth=16, seconds=0.0)
    assert not stopped.solved and stopped.reason == "time budget exhausted"


def test_step_decoder_gives_the_logits_of_the_full_decoder():
    """Sampling decodes one position at a time from cached keys and values; that must not change the answer."""
    from alphafe.model import StepDecoder
    from alphafe.tokenizer import BOS, PAD

    torch.manual_seed(0)
    model = PolicyValueNet(ModelConfig(d_model=32, n_heads=4, enc_layers=1, dec_layers=2, d_ff=64)).eval()
    states, k, length = 3, 2, 11                     # 11 positions: the cache has to grow once
    src = torch.randint(4, model.config.vocab_size, (states, 20))
    src[1, 12:] = PAD                                # a shorter state, so the padding mask matters
    moves = torch.randint(4, model.config.vocab_size, (states * k, length))
    moves[:, 0] = BOS
    with torch.no_grad():
        memory, pad = model.encode(src)
        full = model.decode(memory.repeat_interleave(k, dim=0), pad.repeat_interleave(k, dim=0), moves)
        decoder = StepDecoder(model, memory, pad, k)
        for position in range(length):
            logits = decoder.step(moves[:, position], position)
            assert torch.allclose(logits, full[:, position], atol=1e-4), position
    model.train()
    with pytest.raises(ValueError):
        StepDecoder(model, memory, pad, k)


def test_the_grid_puts_every_piece_of_a_state_on_its_own_row():
    from alphafe.tokenizer import PIECE_STARTS, TOKEN_ID, VOCAB

    model = PolicyValueNet(TINY)
    views = [view_of("f(x+y) = f(x) + y"), view_of("f(x)f(y) = f(x+y) + xy")]
    src = pad_batch([view.tokens for view in views], multiple=64)
    row, column, rows = model.layout(src)
    starts = {TOKEN_ID[token] for token in PIECE_STARTS}
    width = TINY.row_width
    for b, view in enumerate(views):
        expected_row, expected_column = -1, 0
        cells = set()
        for s, token in enumerate(view.tokens):
            if token in starts or expected_column == width:
                expected_row, expected_column = expected_row + 1, 0
            assert (int(row[b, s]), int(column[b, s])) == (expected_row, expected_column), (VOCAB[token], s)
            cells.add((expected_row, expected_column))
            expected_column += 1
        assert len(cells) == len(view.tokens)                       # no two tokens share a cell
        assert expected_row < rows - 1                               # the last row is kept for padding
        assert all(int(row[b, s]) == rows - 1 for s in range(len(view.tokens), src.size(1)))
    assert rows % 8 == 0


def test_a_piece_longer_than_a_row_is_read_as_several_rows():
    from alphafe.tokenizer import TOKEN_ID

    model = PolicyValueNet(TINY)
    width = TINY.row_width
    tokens = [BOS, TOKEN_ID["DOM_R"], TOKEN_ID["SOLVE"], TOKEN_ID["P"]] + [TOKEN_ID["x"]] * (2 * width + 5) + [TOKEN_ID["R1"], TOKEN_ID["y"]]
    row, column, rows = model.layout(torch.tensor([tokens]))
    assert row[0].tolist() == [0, 0, 0] + [1] * width + [2] * width + [3] * 6 + [4, 4]
    assert column[0, 3:3 + width].tolist() == list(range(width)) and column[0, -2:].tolist() == [0, 1]
    memory, pad = model.eval().encode(torch.tensor([tokens]))
    assert memory.shape == (1, len(tokens), TINY.d_model) and torch.isfinite(memory).all() and not pad.any()


def test_a_state_is_encoded_the_same_alone_and_in_a_batch():
    model = PolicyValueNet(TINY).eval()
    short, long = view_of("f(x+y) = f(x) + y"), view_of("f(x)f(y) = f(x+y) + xy")
    with torch.no_grad():
        alone, _ = model.encode(pad_batch([short.tokens]))
        together, pad = model.encode(pad_batch([long.tokens, short.tokens], multiple=64))
    assert torch.allclose(alone[0], together[1, :len(short.tokens)], atol=1e-5)
    assert pad[1, len(short.tokens):].all() and not pad[1, :len(short.tokens)].any()


def test_every_identity_of_a_large_state_is_shown(monkeypatch):
    from alphafe import env
    from alphafe.tokenizer import MAX_STATE_TOKENS, _hidden_renaming

    for name in env.ROUTINE:                                         # the full environment: IMO 2015/5 starts with dozens of identities
        monkeypatch.setitem(env.ROUTINE, name, True)
    state, _ = start(Problem.parse("f(x + f(x + y)) + f(xy) = x + f(x + y) + y*f(x)"))
    assert not state.solved
    view = encode_state(state)
    rows = state.current.rows
    wanted = [row for row in rows if not _hidden_renaming(row, set(rows))]
    assert len(wanted) > 14 and len(view.tokens) <= MAX_STATE_TOKENS
    assert len(view.row_index) == len(wanted)
    memory, _ = PolicyValueNet(TINY).eval().encode(pad_batch([view.tokens]))
    assert memory.shape[1] == len(view.tokens) and torch.isfinite(memory).all()
