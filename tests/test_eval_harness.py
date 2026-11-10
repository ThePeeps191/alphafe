"""The evaluation harness: suite selection, provenance, answer mismatches, flagged problems, budgets."""

import json
from dataclasses import asdict

import pytest

from alphafe import bench
from alphafe import eval as ev
from alphafe.solutions import parse_solution_set

GOOD = {"id": "r1", "equation": "f(x+y) = f(x) + y", "domain": "R", "solutions": ["f(x) = x + c"], "mohs": 0, "source": "t"}
HELD = {"id": "h1", "equation": "f(xy) = x*f(y)", "domain": "R", "tier": 1, "planted": "f(x) = x", "key": "00",
        "source": "synthetic-tier1"}


@pytest.fixture
def tree(tmp_path, monkeypatch):
    """A scratch benchmark tree: one seed problem, two real ones (one flagged), one held-out one."""
    for name in ("seed", "real", "synthetic"):
        (tmp_path / name).mkdir()
    (tmp_path / "seed" / "s.jsonl").write_text(json.dumps(GOOD) + "\n")
    real = [dict(GOOD, id="plain"), dict(GOOD, id="flagged", equation="f(x+y) = f(y) + x", seen_in_development=True)]
    (tmp_path / "real" / "real.jsonl").write_text("\n".join(json.dumps(r) for r in real) + "\n")
    (tmp_path / "synthetic" / "heldout.jsonl").write_text(json.dumps(HELD) + "\n")
    monkeypatch.setattr(bench, "BENCH_DIR", tmp_path)
    monkeypatch.setattr(ev, "RESULTS_DIR", tmp_path / "results")
    return tmp_path


def run(tree, **kwargs):
    options = dict(baseline_budgets=(64,), device="cpu", workers=1)
    options.update(kwargs)
    return ev.full_eval(tree / "missing.pt", options.pop("tag", "t"), **options)


def test_one_suite_can_be_evaluated_alone(tree):
    result = run(tree, suites=["real"], tag=None)
    assert set(result.results) == {"real"}
    names = sorted(p.name for p in (tree / "results").glob("*.json"))
    assert names and all(name.startswith("real_") and not name.startswith("real_real") for name in names)
    assert set(run(tree, suites=["synthetic"]).results) == {"synthetic-tier1"}
    assert set(run(tree, suites=["seed", "synthetic-tier1"]).results) == {"seed", "synthetic-tier1"}
    assert set(run(tree).results) == {"seed", "real", "synthetic-tier1"}
    with pytest.raises(ValueError, match="unknown suite"):
        run(tree, suites=["reel"])


def test_result_files_say_what_produced_them(tree):
    run(tree, suites=["real"])
    payload = json.loads((tree / "results" / "t_real_brute_force_64_calls.json").read_text())
    stamp = payload["provenance"]
    for key in ("commit", "dirty", "time_utc", "python", "platform", "torch", "device", "checkpoint", "checkpoint_sha256"):
        assert key in stamp, key
    assert stamp["device"] == "cpu" and stamp["checkpoint"] is None       # no checkpoint was loaded
    settings = stamp["settings"]
    assert settings["suites"] == ["real"] and settings["baseline_budgets"] == [64]
    assert settings["sampling_seeds"] == [1000] and settings["proposals_per_state"] == ev.PROPOSALS
    # Committed files must not carry a home directory.
    assert str(tree) not in json.dumps(payload) and str(ev.ROOT) not in json.dumps(payload)


def test_checkpoint_is_recorded_by_hash_and_portable_path(tmp_path):
    inside = ev.ROOT / "checkpoints" / "example.pt"
    assert ev._portable_path(inside) == "checkpoints/example.pt"
    outside = tmp_path / "weights.pt"
    outside.write_bytes(b"abc")
    assert ev._portable_path(outside) == "weights.pt"
    stamp = ev.provenance(outside, "cpu", {"k": 1})
    assert stamp["checkpoint"] == "weights.pt" and stamp["settings"] == {"k": 1}
    assert stamp["checkpoint_sha256"] == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_saved_answers_can_be_read_back(tree):
    result = run(tree, suites=["seed"])
    rows = result.results["seed"]["brute force (64 calls)"]
    assert rows[0].solved and parse_solution_set(rows[0].solutions) == bench.load_seed()[0].expected
    saved = json.loads((tree / "results" / "t_seed_brute_force_64_calls.json").read_text())
    assert saved["rows"][0]["solutions"] == rows[0].solutions == ["f(x) = x + c"]


def test_flagged_problems_are_reported_separately(tree):
    result = run(tree, suites=["real"])
    rows = result.results["real"]["brute force (64 calls)"]
    assert [r.flags for r in rows] == [[], ["seen_in_development"]]
    text = ev.report(result.results, result.spreads, result.seed_rows)
    assert "#### real (2 problems)" in text
    assert "Without the 1 flagged problems (1 seen in development): 1 problems" in text
    assert text.count("| brute force (64 calls) |") == 4      # summary and MOHS tables, each given twice
    saved = json.loads((tree / "results" / "t_real_brute_force_64_calls.json").read_text())
    assert saved["summary"]["problems"] == 2 and saved["summary_unflagged"]["problems"] == 1
    # A suite without flags gets one set of tables.
    assert "Without the" not in ev.report(run(tree, suites=["seed"]).results)


def wrong_answer(tree):
    """Record f(x) = x for the first real problem; its full answer is f(x) = x + c."""
    records = [dict(GOOD, id="plain", solutions=["f(x) = x"]), dict(GOOD, id="other", equation="f(x+y) = f(y) + x")]
    (tree / "real" / "real.jsonl").write_text("\n".join(json.dumps(r) for r in records) + "\n")


def test_an_answer_mismatch_is_kept_with_its_proof_and_the_run_survives(tree):
    wrong_answer(tree)
    found: list = []
    result = run(tree, suites=["real"], mismatches=found)
    rows = result.results["real"]["brute force (64 calls)"]
    assert not rows[0].solved and rows[0].reason == ev.MISMATCH_REASON and rows[0].answer == "" and rows[0].proof == ""
    assert rows[1].solved                                   # the other problem's row is intact
    assert found and all(item["id"] == "plain" for item in found)
    item = next(i for i in found if i["solver"] == "brute force (64 calls)")
    assert item["recorded"] == ["f(x) = x"] and item["found"] == ["f(x) = x + c"] and "conclude" in item["proof"]
    files = sorted((tree / "results").glob("t_MISMATCH_plain_*.json"))
    assert len(files) == len(found) and "conclude" in json.loads(files[0].read_text())["proof"]
    assert "accepted proof" in ev.mismatch_text(found)
    # The summary never counts a mismatch as solved.
    assert json.loads((tree / "results" / "t_real_brute_force_64_calls.json").read_text())["summary"]["solved"] == 1


def test_without_a_collector_the_mismatch_is_raised_after_saving(tree):
    wrong_answer(tree)
    with pytest.raises(bench.AnswerMismatch, match="accepted proof"):
        run(tree, suites=["real"])
    assert (tree / "results" / "t_real_brute_force_64_calls.json").exists()
    with pytest.raises(bench.AnswerMismatch, match="conclude"):         # a direct call still raises at once
        ev.run_baseline(bench.load_real(), 64, 20, workers=1)


def test_the_command_line_exits_nonzero_on_a_mismatch(tree, monkeypatch, capsys):
    wrong_answer(tree)
    monkeypatch.setattr(ev, "tree_is_dirty", lambda: False)
    monkeypatch.setattr(ev, "ROOT", tree)                   # so that no default checkpoint is found
    with pytest.raises(SystemExit) as stop:
        ev.main(["--suite", "real", "--device", "cpu", "--workers", "1"])
    assert stop.value.code == 2
    captured = capsys.readouterr()
    assert "#### real (2 problems)" in captured.out and "accepted proof" in captured.err
    assert (tree / "results" / "real.md").exists()


def test_big_budget_rows(tree):
    with pytest.raises(ValueError, match="standard row"):
        run(tree, big_budget=ev.SEARCH_BUDGET)
    with pytest.raises(ValueError, match="standard row"):
        run(tree, big_budget=ev.GREEDY_BUDGET)
    result = run(tree, big_budget=70)
    assert "brute force (70 calls)" in result.results["seed"] and "brute force (70 calls)" in result.results["real"]
    assert "brute force (70 calls)" not in result.results["synthetic-tier1"]
    assert "brute force (64 calls)" in result.results["synthetic-tier1"]


def test_command_line_refuses_a_missing_checkpoint_and_a_dirty_tree(tree, monkeypatch, capsys):
    monkeypatch.setattr(ev, "tree_is_dirty", lambda: False)
    with pytest.raises(SystemExit) as stop:
        ev.main(["--checkpoint", str(tree / "typo.pt"), "--suite", "seed"])
    assert stop.value.code == 2 and "no checkpoint at" in capsys.readouterr().err
    with pytest.raises(SystemExit):
        ev.main(["--big-budget", "128", "--suite", "seed"])
    assert "standard row" in capsys.readouterr().err
    monkeypatch.setattr(ev, "tree_is_dirty", lambda: True)
    with pytest.raises(SystemExit):
        ev.main(["--suite", "seed"])
    assert "uncommitted changes" in capsys.readouterr().err
    assert not (tree / "results").exists()                  # nothing was run


def test_network_rows_keep_every_sampling_seed(tree, monkeypatch):
    """With a checkpoint: every sampling seed's outcome is saved, and the file names the weights by hash."""
    import torch

    from alphafe.model import ModelConfig, PolicyValueNet

    torch.manual_seed(0)
    tiny = ModelConfig(d_model=32, n_heads=2, enc_layers=1, dec_layers=1, d_ff=64)
    path = tree / "tiny.pt"
    torch.save({"config": asdict(tiny), "model": PolicyValueNet(tiny).state_dict()}, path)
    result = ev.full_eval(path, "t", baseline_budgets=(64,), device="cpu", workers=1, seeds=2, suites=["real"])
    label = f"network, search ({ev.SEARCH_BUDGET} calls)"
    assert len(result.spreads["real"][label]) == 2 and len(result.seed_rows["real"][label]) == 2
    saved = json.loads((tree / "results" / "t_real_network_search_128_calls.json").read_text())
    assert len(saved["per_seed"]) == 2 and set(saved["per_seed"][0]) == {"plain", "flagged"}
    assert saved["per_seed"][0]["plain"] == [int(saved["rows"][0]["solved"]), saved["rows"][0]["checker_calls"]]
    assert saved["config"]["solved_per_seed"] == result.spreads["real"][label]
    assert saved["provenance"]["checkpoint"] == "tiny.pt" and len(saved["provenance"]["checkpoint_sha256"]) == 64
    assert saved["provenance"]["settings"]["sampling_seeds"] == [1000, 1001]
    brute = json.loads((tree / "results" / "t_real_brute_force_64_calls.json").read_text())
    assert "per_seed" not in brute and brute["config"]["checkpoint"] is None
