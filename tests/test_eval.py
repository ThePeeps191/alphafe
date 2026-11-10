import random

from alphafe.bench import load_seed
from alphafe.eval import markdown_by_mohs, markdown_summary, report, run_policy, summary
from alphafe.search import UniformProposer


def test_run_policy_scores_with_the_canary_and_formats_tables():
    seeds = load_seed()[:5]
    rows = run_policy(seeds, UniformProposer(random.Random(0)), "search", budget=200)
    assert len(rows) == 5 and all(r.checker_calls <= 200 for r in rows)
    solved = [r for r in rows if r.solved]
    assert len(solved) >= 3 and all(r.proof and r.answer for r in solved)
    greedy = run_policy(seeds, UniformProposer(random.Random(0)), "greedy", budget=32)
    runs = {"search": rows, "greedy": greedy}
    table = markdown_summary(runs)
    assert table.count("\n") == 3 and "| search |" in table
    assert "0M" in markdown_by_mohs(runs)
    text = report({"seed": runs})
    assert "#### seed (5 problems)" in text
    assert summary(rows)["problems"] == 5


def test_real_benchmark_files_are_picked_up(tmp_path, monkeypatch):
    """Whatever the owners drop into benchmarks/real/ is loaded, scored and tabulated,
    including records without a recorded answer or MOHS estimate."""
    import json

    from alphafe import bench
    from alphafe.eval import by_mohs, run_baseline

    real = tmp_path / "real"
    real.mkdir()
    (real / "mine.jsonl").write_text("\n".join(json.dumps(r) for r in [
        {"id": "r1", "equation": "f(x+y) = f(x) + y", "domain": "R", "solutions": ["f(x) = x + c"], "mohs": 0, "source": "test"},
        {"id": "r2", "equation": "f(xy) = x*f(y)", "domain": "R", "source": "test"},
    ]) + "\n# a comment line\n")
    monkeypatch.setattr(bench, "BENCH_DIR", tmp_path)
    benches = bench.load_real()
    assert [b.id for b in benches] == ["r1", "r2"]
    assert benches[0].expected is not None and benches[1].expected is None and benches[1].mohs is None
    rows = run_baseline(benches, max_calls=300, max_seconds=20, workers=1)
    assert all(r.solved for r in rows)
    assert by_mohs(rows) == {"0M": [1, 1], "?": [1, 1]}
    text = markdown_by_mohs({"brute force": rows})
    assert "?" in text and "0M" in text


def test_real_benchmark_answers_are_checked_by_the_canary(tmp_path, monkeypatch):
    import json

    import pytest

    from alphafe import bench
    from alphafe.eval import run_baseline

    real = tmp_path / "real"
    real.mkdir()
    (real / "wrong.jsonl").write_text(json.dumps(
        {"id": "w1", "equation": "f(x+y) = f(x) + y", "domain": "R", "solutions": ["f(x) = x"], "source": "test"}) + "\n")
    monkeypatch.setattr(bench, "BENCH_DIR", tmp_path)
    with pytest.raises(bench.AnswerMismatch):       # the recorded answer misses f(x) = x + c
        run_baseline(bench.load_real(), max_calls=300, max_seconds=20, workers=1)


def test_frozen_heldout_set_is_disjoint_from_any_training_pool():
    from alphafe.eval import common_calls, synthetic_heldout
    from alphafe.generate import benchmark_keys, canonical_key
    from alphafe.train import ProblemPool

    heldout = synthetic_heldout(limit=200)
    assert sorted(heldout) == [1, 2, 3, 4] and all(len(v) == 200 for v in heldout.values())
    keys = {b.meta["key"] for benches in heldout.values() for b in benches}
    assert len(keys) == 800
    for benches in list(heldout.values())[:2]:
        for b in benches[:25]:
            assert canonical_key(b.problem.poly) == b.meta["key"]
            assert int(b.meta["key"][:8], 16) % 10 == 0       # the "test" side of the hash split
    assert not keys & benchmark_keys()
    pool = ProblemPool(seed=7, per_tier=80)
    train_keys = {g.key for items in pool.train.values() for g in items}
    assert not train_keys & keys


def test_common_calls_compares_like_with_like():
    from alphafe.eval import Row, common_calls

    def row(i, solved, calls):
        return Row(i, "", "R", None, solved, calls, 0.0, 0, "", "")

    a = [row("p", True, 2), row("q", True, 100), row("r", False, 50)]
    b = [row("p", True, 10), row("q", False, 50), row("r", True, 4)]
    assert common_calls(a, b) == (1, 2.0, 10.0)
    assert common_calls(a, [row("z", True, 1)]) is None
