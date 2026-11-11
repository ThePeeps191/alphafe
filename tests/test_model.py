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
