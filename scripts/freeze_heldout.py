"""Write the held-out synthetic test problems to benchmarks/synthetic/heldout.jsonl.

    .venv/bin/python scripts/freeze_heldout.py --check     # regenerate in memory and compare with the file
    .venv/bin/python scripts/freeze_heldout.py --force     # overwrite the file

The held-out file is the benchmark every table is measured on, so it is
frozen in a file and not regenerated. Without --force this script never
writes. The generator's output can shift when the checker or the benchmark
files change (it drops problems the free moves solve outright and skips
benchmark problems), so --check may report a difference without anything
being wrong; the committed file stays the reference. Every problem in the
file has split == "test" by its canonical hash, so no training pool can
contain it.
"""
import argparse
import json
import sys

from alphafe.bench import BENCH_DIR
from alphafe.train import ProblemPool

PER_TIER = 200


def lines() -> list:
    pool = ProblemPool(seed=0, per_tier=3000)
    out = []
    for tier, items in pool.test.items():
        for g in items[:PER_TIER]:
            assert g.split == "test"
            out.append(json.dumps({"id": g.key[:10], "equation": g.equation, "domain": g.domain, "tier": g.tier,
                                   "planted": g.planted, "key": g.key, "source": f"synthetic-tier{g.tier}"}))
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Regenerate the frozen held-out set (compare by default).")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="compare a fresh generation with the file (the default)")
    group.add_argument("--force", action="store_true", help="overwrite benchmarks/synthetic/heldout.jsonl")
    args = parser.parse_args()
    path = BENCH_DIR / "synthetic" / "heldout.jsonl"
    fresh = lines()
    if args.force:
        path.write_text("\n".join(fresh) + "\n")
        print("wrote", path)
        sys.exit(0)
    current = path.read_text().splitlines() if path.exists() else []
    same = sum(a == b for a, b in zip(current, fresh))
    if current == fresh:
        print(f"{path.name}: a fresh generation gives the same {len(fresh)} problems")
        sys.exit(0)
    print(f"{path.name}: {len(current)} problems in the file, {len(fresh)} generated now, {same} identical line for line")
    print("The file was not changed. Use --force to overwrite it (this redefines the benchmark).")
    sys.exit(1)
