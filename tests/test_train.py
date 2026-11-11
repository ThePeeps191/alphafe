import json
import random
import shutil

import pytest

torch = pytest.importorskip("torch")      # the network tests need torch; the rest of the suite does not

from alphafe import train as train_module
from alphafe.checker import Problem
from alphafe.generate import benchmark_keys
from alphafe.search import BestFirstSearch, UniformProposer, run_searches
from alphafe.tokenizer import EOS, TOKEN_ID
from alphafe.train import ProblemPool, ReplayBuffer, TrainConfig, harvest, make_batch, train

pytestmark = pytest.mark.usefixtures("plain_environment")      # see tests/conftest.py

TINY_MODEL = dict(d_model=32, n_heads=2, enc_layers=1, dec_layers=1, d_ff=64, dropout=0.0, vocab_size=len(TOKEN_ID),
                  max_src=448, max_tgt=56)


def test_pool_split_is_disjoint_and_excludes_benchmarks():
    pool = ProblemPool(seed=5, per_tier=60)
    train_keys = {g.key for items in pool.train.values() for g in items}
    test_keys = {g.key for items in pool.test.values() for g in items}
    assert train_keys and test_keys and not train_keys & test_keys
    assert not (train_keys | test_keys) & benchmark_keys()
    rng = random.Random(0)
    sampled = pool.sample_train(rng, 3, 200)
    assert all(g.split == "train" and g.tier <= 3 for g in sampled)


def test_harvest_builds_the_three_kinds_of_examples():
    rng = random.Random(0)
    solved = BestFirstSearch(Problem.parse("f(x+y) = f(x) + y"), budget=300)
    failed = BestFirstSearch(Problem.parse("f(x-y) = f(x)f(y)", "R"), budget=30)
    run_searches([solved, failed], UniformProposer(rng), k=8)
    assert solved.solved_node is not None and failed.solved_node is None
    buffer = ReplayBuffer(1000)
    harvest([solved, failed], buffer, rng, minimise=False)
    assert len(buffer.solve) == len(solved.solution_path()) - 1 >= 1
    assert buffer.negative and buffer.hindsight
    for src, tgt in buffer.solve + buffer.hindsight:
        assert tgt[-1] == EOS
    assert all(src[2] == TOKEN_ID["SOLVE"] for src, _ in buffer.solve)
    assert all(src[2] == TOKEN_ID["GOAL"] for src, _ in buffer.hindsight)
    config = TrainConfig(batch_size=16)
    pieces = make_batch(buffer, config, rng, torch.device("cpu"))
    assert sum(src.shape[0] for src, *_ in pieces) == 16
    widths = [src.shape[1] for src, *_ in pieces]
    assert widths == sorted(widths)                       # length-sorted pieces
    for src, tgt_in, tgt_out, value, mask in pieces:
        assert src.shape[0] == tgt_in.shape[0] == value.shape[0] and tgt_in.shape == tgt_out.shape


def test_minimal_examples_drop_useless_moves():
    """A proof found with a detour is cut down to the moves that matter."""
    from alphafe.search import Node
    from alphafe.env import step
    from alphafe.moves import parse_move
    from alphafe.tokenizer import encode_move
    from alphafe.train import minimal_examples

    search = BestFirstSearch(Problem.parse("f(x+y) = f(x) + y"), budget=10)
    node = search.root
    for text in ["sub P: y:=1", "sub P: x:=0"]:      # the first move is not needed
        move = parse_move(text)
        ids = encode_move(move, node.view)
        state, applied = step(node.state, move)
        node = Node(state, node.proof + applied, node, ids, 0.0, node.depth + 1)
    assert node.state.solved
    search.solved_node = node
    pairs = minimal_examples(search)
    assert len(pairs) == 1
    src, tgt = pairs[0]
    assert tgt == tuple(encode_move(parse_move("sub P: x:=0"), search.root.view))
    assert src == tuple(search.root.view.tokens)


def test_swapped_examples_mirror_a_proof():
    from alphafe.env import start
    from alphafe.moves import parse_move
    from alphafe.tokenizer import decode_move, encode_state
    from alphafe.train import swapped_examples

    problem = Problem.parse("f(x+y) = f(x) + y")
    pairs = swapped_examples(problem, [parse_move("sub P: x:=0")])
    assert len(pairs) == 1
    mirror = Problem.parse("f(x+y) = f(y) + x")
    state, _ = start(mirror)
    view = encode_state(state)
    assert pairs[0][0] == tuple(view.tokens)                      # the mirrored problem's own start state
    assert decode_move(list(pairs[0][1]), view) == parse_move("sub P: y:=0")
    # a proof that does not solve the problem yields nothing
    assert swapped_examples(problem, [parse_move("sub P: y:=1")]) == []


def test_swapped_examples_follow_row_targets_and_splits():
    from alphafe.moves import parse_move
    from alphafe.train import swapped_examples

    problem = Problem.parse("f(x)f(y) = f(xy) + x + y")
    moves = [parse_move(t) for t in ["sub P: x:=0, y:=0", "split R1", "sub P: y:=0", "sub P: y:=0"]]
    pairs = swapped_examples(problem, moves)
    assert len(pairs) == 4


@pytest.mark.slow
def test_training_runs_checkpoints_and_resumes(tmp_path, monkeypatch):
    monkeypatch.setattr(train_module, "ROOT", tmp_path)
    config = TrainConfig(run="t", per_tier=40, iterations=2, problems_per_iter=12, budget=16, steps_per_iter=3,
                         batch_size=8, eval_every=1, eval_problems=4, device="cpu", model=TINY_MODEL, minutes=5)
    record = train(config)
    assert record["iteration"] == 2 and "heldout_t1_greedy" in record
    assert (tmp_path / "checkpoints" / "t" / "last.pt").exists()
    # The replay buffer is stored as plain lists (buffer.pt); it used to be a pickle (buffer.pkl).
    assert (tmp_path / "checkpoints" / "t" / "buffer.pt").exists()
    assert not (tmp_path / "checkpoints" / "t" / "buffer.pkl").exists()
    lines = (tmp_path / "logs" / "t" / "train.jsonl").read_text().splitlines()
    assert len(lines) == 2 and json.loads(lines[0])["iteration"] == 1
    config.iterations = 3
    resumed = train(config, resume=True)
    assert resumed["iteration"] == 3


def tiny_run(tmp_path, monkeypatch, **changes):
    monkeypatch.setattr(train_module, "ROOT", tmp_path)
    settings = dict(run="t", per_tier=40, iterations=1, problems_per_iter=12, budget=16, steps_per_iter=2,
                    batch_size=8, eval_every=1, eval_problems=4, device="cpu", model=TINY_MODEL, minutes=5)
    settings.update(changes)
    return TrainConfig(**settings)


def test_progress_prefers_untried_problems_and_lets_hopeless_ones_fade():
    from alphafe.train import Progress

    progress = Progress(["a", "b", "c"])
    assert [progress.weight(i) for i in range(3)] == [1.0, 1.0, 1.0]
    assert progress.record(0, True) is True and progress.record(0, True) is False      # only the first solution is "first"
    for _ in range(3):
        progress.record(1, False)
    assert progress.weight(1) == 0.25 and progress.weight(2) == 1.0
    assert 0 < progress.weight(0) < Progress.SOLVED_WEIGHT
    progress.record(0, False)                              # a later failure does not unsolve a problem
    assert progress.fails[0] == 0 and progress.known() == 1
    picks = progress.sample(random.Random(0), 300)
    assert picks.count(2) > picks.count(1) > 0
    with pytest.raises(ValueError):
        Progress(["a"], fails=[0, 0], solved=[0])


@pytest.mark.slow
def test_adaptive_curriculum_runs_and_resumes_with_its_progress(tmp_path, monkeypatch):
    config = tiny_run(tmp_path, monkeypatch, curriculum="adaptive", iterations=2)
    record = train(config)
    assert record["tier"] == 4 and "known_solved" in record and "heldout_t4_greedy" in record
    payload = torch.load(tmp_path / "checkpoints" / "t" / "last.pt", weights_only=True)
    attempts = sum(payload["state"]["fails"]) + sum(payload["state"]["solved"])
    assert 0 < attempts <= 24                               # two iterations of twelve problems
    config.iterations = 3
    assert train(config, resume=True)["iteration"] == 3
    with pytest.raises(ValueError, match="curriculum"):
        train(tiny_run(tmp_path, monkeypatch, run="u", curriculum="ladder"))


@pytest.mark.slow
def test_resume_restores_the_replay_buffer_and_the_random_stream(tmp_path, monkeypatch, capsys):
    config = tiny_run(tmp_path, monkeypatch)
    train(config)
    ckpt = tmp_path / "checkpoints" / "t"
    stored = torch.load(ckpt / "buffer.pt", map_location="cpu", weights_only=True)
    sizes = [len(store) for store in stored]
    assert sum(sizes) > 0
    config.iterations = 2
    capsys.readouterr()
    train(config, resume=True)
    assert f"{sum(sizes)} examples" in capsys.readouterr().out        # the whole buffer came back


@pytest.mark.slow
def test_resume_never_runs_code_from_the_checkpoint_or_the_buffer(tmp_path, monkeypatch):
    """A downloaded checkpoint put at checkpoints/<run>/last.pt to continue training must not be able to run code."""
    import pathlib

    config = tiny_run(tmp_path, monkeypatch)
    train(config)
    ckpt = tmp_path / "checkpoints" / "t"

    class Payload:
        def __reduce__(self):
            return (pathlib.Path.touch, (tmp_path / "ran",))

    good = torch.load(ckpt / "last.pt", map_location="cpu", weights_only=True)
    torch.save({**good, "extra": Payload()}, ckpt / "last.pt")
    with pytest.raises(Exception):
        train(config, resume=True)
    assert not (tmp_path / "ran").exists()
    torch.save(good, ckpt / "last.pt")
    torch.save([[Payload()], [], []], ckpt / "buffer.pt")
    with pytest.raises(Exception):
        train(config, resume=True)
    assert not (tmp_path / "ran").exists()
    # An old pickle buffer is left alone, with a message, instead of being unpickled.
    (ckpt / "buffer.pt").unlink()
    import pickle
    (ckpt / "buffer.pkl").write_bytes(pickle.dumps(Payload()))
    config.iterations = 2
    train(config, resume=True)
    assert not (tmp_path / "ran").exists()


@pytest.mark.slow
def test_training_can_continue_from_a_weights_only_export(tmp_path, monkeypatch, capsys):
    from alphafe.model import export_checkpoint

    config = tiny_run(tmp_path, monkeypatch)
    train(config)
    ckpt = tmp_path / "checkpoints" / "t"
    export_checkpoint(ckpt / "last.pt", ckpt / "slim.pt")
    (ckpt / "slim.pt").replace(ckpt / "last.pt")
    (ckpt / "buffer.pt").unlink()
    config.iterations = 2
    capsys.readouterr()
    record = train(config, resume=True)                                # used to fail with KeyError: 'optimizer'
    assert record["iteration"] == 2 and "weights-only export" in capsys.readouterr().out


def test_set_overrides_are_read_exactly_or_refused():
    from alphafe.train import apply_overrides

    config = TrainConfig()
    apply_overrides(config, ["mirror=false", "diverse=0", "minimise=No", "budget=64", "lr=0.001", "run=abc"])
    assert (config.mirror, config.diverse, config.minimise, config.budget, config.lr, config.run) == (False, False, False, 64, 0.001, "abc")
    apply_overrides(config, ["mirror=true", "diverse=1", "minimise=YES"])      # "true" used to mean False
    assert config.mirror and config.diverse and config.minimise
    for bad, message in [("mirror=maybe", "mirror is on or off"), ("nosuch=1", "unknown setting"),
                         ("model={}", "unknown setting"), ("budget=many", "budget takes int values"), ("budget", "expected KEY=VALUE")]:
        with pytest.raises(ValueError, match=message):
            apply_overrides(config, [bad])


def test_train_command_line_reports_a_bad_override(capsys, monkeypatch):
    seen = {}
    monkeypatch.setattr(train_module, "train", lambda config, resume=False: seen.update(config=config))
    train_module.main(["--run", "x", "--set", "mirror=false", "--set", "budget=64"])
    assert seen["config"].mirror is False and seen["config"].budget == 64
    assert "mirror=False" in capsys.readouterr().out
    with pytest.raises(SystemExit) as stop:
        train_module.main(["--run", "x", "--set", "mirror=tru"])
    assert stop.value.code == 2 and "mirror is on or off" in capsys.readouterr().err
