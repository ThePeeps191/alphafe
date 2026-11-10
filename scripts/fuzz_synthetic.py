"""Model-check fuzz on synthetic problems: random moves vs the planted solution.

Usage: fuzz_synthetic.py [problems per tier] [steps] [walks per problem]
"""
import random
import sys
import time

sys.path.insert(0, ".")
from alphafe.generate import generate
from alphafe.solutions import parse_solution
from tests.test_modelcheck import walk

per_tier = int(sys.argv[1]) if len(sys.argv) > 1 else 150
steps = int(sys.argv[2]) if len(sys.argv) > 2 else 60
walks = int(sys.argv[3]) if len(sys.argv) > 3 else 3
rng = random.Random(2024)
began = time.time()
accepted = count = 0
for tier, items in generate(seed=99, per_tier=per_tier).items():
    for item in items:
        expr = parse_solution(item.planted)
        for _ in range(walks):
            try:
                accepted += walk(item.problem(), expr, rng, steps)
            except Exception as err:
                print("FAILURE", item.equation, item.domain, item.planted, "->", type(err).__name__, err)
                raise
            count += 1
print(f"{count} walks, {accepted} accepted moves, {time.time() - began:.1f}s, no violation")
