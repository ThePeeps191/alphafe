"""Long model-check fuzz run (see tests/test_modelcheck.py and tests/nonpoly.py).

    .venv/bin/python scripts/fuzz.py [rounds] [steps] [--seed N]

Random moves are fired at the checker and every accepted state is tested:
first against the polynomial answers of the seed problems, then against
solutions that are not polynomials (|x|, 1/x, wild additive functions, ...),
which no accepted sequence of moves may lose. Another --seed gives other walks.
"""
import argparse
import pathlib
import random
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))      # the tests package, from any directory

parser = argparse.ArgumentParser(description="Model-check fuzzing of the checker.")
parser.add_argument("rounds", nargs="?", type=int, default=20, help="walks per (problem, solution) pair")
parser.add_argument("steps", nargs="?", type=int, default=80, help="moves tried per walk")
parser.add_argument("--seed", type=int, default=12345, help="seed of the random walks (default 12345)")
args = parser.parse_args()

from alphafe.checker import Problem
from tests import nonpoly
from tests.seedlib import seed_problem
from tests.test_modelcheck import CASES, instantiate, random_move, walk

rng = random.Random(args.seed)
start = time.time()
accepted = walks = 0
for r in range(args.rounds):
    for record, solution in CASES:
        problem = seed_problem(record)
        expr = instantiate(solution, rng)
        try:
            accepted += walk(problem, expr, rng, args.steps)
        except Exception as err:
            print("FAILURE", record["id"], record["equation"], "f(x) =", expr, "->", type(err).__name__, err)
            raise
        walks += 1
print(f"polynomial models: {walks} walks, {accepted} accepted moves, {time.time() - start:.1f}s, no violation")

start = time.time()
accepted = walks = 0
for r in range(args.rounds):
    for equation, domain, model in nonpoly.CASES:
        try:
            accepted += nonpoly.walk(Problem.parse(equation, domain), model, rng, args.steps, random_move)
        except Exception as err:
            print("FAILURE", equation, domain, "f =", model.name, "->", type(err).__name__, err)
            raise
        walks += 1
print(f"non-polynomial models: {walks} walks, {accepted} accepted moves, {time.time() - start:.1f}s, no violation")
