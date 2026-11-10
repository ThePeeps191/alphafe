"""Long model-check fuzz run (see tests/test_modelcheck.py). Usage: fuzz.py [rounds] [steps]"""
import random
import sys
import time

sys.path.insert(0, ".")
from tests.seedlib import load_seeds, seed_problem
from tests.test_modelcheck import CASES, instantiate, walk

rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 20
steps = int(sys.argv[2]) if len(sys.argv) > 2 else 80
rng = random.Random(12345)
start = time.time()
accepted = walks = 0
for r in range(rounds):
    for record, solution in CASES:
        problem = seed_problem(record)
        expr = instantiate(solution, rng)
        try:
            accepted += walk(problem, expr, rng, steps)
        except Exception as err:
            print("FAILURE", record["id"], record["equation"], "f(x) =", expr, "->", type(err).__name__, err)
            raise
        walks += 1
print(f"{walks} walks, {accepted} accepted moves, {time.time() - start:.1f}s, no violation")
