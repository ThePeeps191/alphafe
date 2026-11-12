"""The development suite: valid records, no overlap with the unseen real problems, hand proofs that check."""

import pytest

from alphafe.bench import BENCH_DIR, load_dev, load_dir, load_real, load_seed
from alphafe.benchcheck import validate
from alphafe.checker import check
from alphafe.generate import canonical_key, protected_keys, twin_keys
from alphafe.moves import parse_proof

DEV = {bench.id: bench for bench in load_dev()}
PROOFS = sorted((BENCH_DIR / "dev" / "proofs").glob("*.proof"))


def test_the_dev_file_passes_the_basic_check():
    report = validate(sorted((BENCH_DIR / "dev").glob("*.jsonl")), strict=False)
    assert report.records == len(load_dir("dev")) == 20
    assert report.errors == [] and report.warnings == []


def test_the_suite_is_the_dev_file_plus_the_flagged_real_problems():
    flagged = [b.id for b in load_real() if b.meta.get("seen_in_development")]
    assert len(flagged) == 16 and len(DEV) == 36
    assert set(flagged) <= set(DEV)


def test_no_dev_problem_is_a_twin_of_an_unseen_real_problem_or_of_a_seed_problem():
    """Tuning on a dev problem must not be tuning on a test problem in disguise."""
    taken = {}
    for bench in load_seed() + load_real():
        if bench.meta.get("seen_in_development"):
            continue
        try:
            taken[canonical_key(bench.problem.poly)] = bench.id
        except Exception:           # the two problems the checker refuses to load have no key
            continue
    for bench in load_dir("dev"):
        hits = [taken[key] for key in twin_keys(bench.problem.equation) if key in taken]
        assert not hits, (bench.id, hits)


def test_dev_problems_are_kept_out_of_training():
    keys = protected_keys()
    assert all(canonical_key(bench.problem.poly) in keys for bench in load_dir("dev"))


@pytest.mark.parametrize("path", PROOFS, ids=lambda p: p.stem)
def test_hand_proofs_check_and_give_the_recorded_answer(path):
    bench = DEV[path.stem]
    result = check(bench.problem, parse_proof(path.read_text()))
    assert result.solved and result.solutions == bench.expected
