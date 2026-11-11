"""Check every hand-written proof in benchmarks/seed/proofs and benchmarks/dev/proofs against its problem."""
import sys

from alphafe.bench import BENCH_DIR, load_dev, load_seed
from alphafe.checker import check
from alphafe.moves import parse_proof

if len(sys.argv) > 1:
    sys.exit(__doc__)
bad = 0
for name, benches in (("seed", load_seed()), ("dev", load_dev())):
    by_id = {bench.id: bench for bench in benches}
    for path in sorted((BENCH_DIR / name / "proofs").glob("*.proof")):
        bench = by_id[path.stem]
        result = check(bench.problem, parse_proof(path.read_text()))
        ok = result.solved and result.solutions == bench.expected
        bad += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {path.stem}  {bench.problem.equation:45s} {result}"
              + ("" if ok else f"   expected: {bench.expected}"))
sys.exit(1 if bad else 0)
