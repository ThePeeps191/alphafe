"""Check every hand-written proof in benchmarks/seed/proofs against the seed file."""
import json
import pathlib
import sys

from alphafe.checker import Problem, check
from alphafe.moves import parse_proof
from alphafe.solutions import parse_solution_set

root = pathlib.Path(__file__).resolve().parent.parent / "benchmarks" / "seed"
seeds = {}
for seed_file in sorted(root.glob("*.jsonl")):
    seeds.update({r["id"]: r for r in map(json.loads, seed_file.read_text().splitlines())})
bad = 0
for path in sorted((root / "proofs").glob("*.proof")):
    rec = seeds[path.stem]
    problem = Problem.parse(rec["equation"], rec["domain"], rec["id"])
    result = check(problem, parse_proof(path.read_text()))
    expected = parse_solution_set(rec["solutions"])
    ok = result.solved and result.solutions == expected
    bad += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {path.stem}  {rec['equation']:45s} {result}" + ("" if ok else f"   expected: {expected}"))
sys.exit(1 if bad else 0)
