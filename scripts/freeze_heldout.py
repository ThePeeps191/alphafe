"""Write the held-out synthetic test problems to benchmarks/synthetic/heldout.jsonl.

The generator's output can shift when the checker changes (it drops problems
the free moves solve outright), so the evaluation set is frozen in a file
instead of being regenerated. Every problem in the file has split == "test"
by its canonical hash, so no training pool can ever contain it.
"""
import json

from alphafe.bench import BENCH_DIR
from alphafe.train import ProblemPool

PER_TIER = 200

if __name__ == "__main__":
    pool = ProblemPool(seed=0, per_tier=3000)
    path = BENCH_DIR / "synthetic" / "heldout.jsonl"
    with open(path, "w") as fh:
        for tier, items in pool.test.items():
            for g in items[:PER_TIER]:
                assert g.split == "test"
                fh.write(json.dumps({"id": g.key[:10], "equation": g.equation, "domain": g.domain, "tier": g.tier,
                                     "planted": g.planted, "key": g.key, "source": f"synthetic-tier{g.tier}"}) + "\n")
    print("wrote", path)
