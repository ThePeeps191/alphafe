"""Measure the uniform-random grammar-constrained policy on synthetic tiers (the 'untrained' reference).

Usage: random_policy.py [problems per tier]
"""
import random
import sys
import time

from alphafe.generate import benchmark_keys, generate
from alphafe.search import BestFirstSearch, GreedySearch, UniformProposer, run_searches

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        sys.exit(__doc__)
    per_tier = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    data = generate(0, per_tier, exclude=benchmark_keys())
    for tier, items in data.items():
        problems = [it.problem() for it in items]
        line = [f"tier {tier} ({len(problems)} problems):"]
        for label, make in (
            ("greedy/64", lambda p: GreedySearch(p, budget=64)),
            ("search/64", lambda p: BestFirstSearch(p, budget=64)),
            ("search/256", lambda p: BestFirstSearch(p, budget=256)),
            ("search/1024", lambda p: BestFirstSearch(p, budget=1024)),
        ):
            began = time.time()
            searches = [make(p) for p in problems]
            run_searches(searches, UniformProposer(random.Random(1)), k=8)
            solved = sum(s.solved_node is not None for s in searches)
            calls = sum(s.calls for s in searches)
            line.append(f"{label}: {solved}/{len(problems)} ({time.time() - began:.0f}s, {calls} calls)")
        print("  ".join(line), flush=True)
