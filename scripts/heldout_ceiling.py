"""How many held-out synthetic problems can brute force solve with a large budget?

A rough "known solvable" count per tier, to put the 128- and 2,000-call
numbers in context. Usage: heldout_ceiling.py [checker calls]
"""
import sys
import time

from alphafe.eval import run_baseline, save, summary, synthetic_heldout

if __name__ == "__main__":
    budget = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    for tier, benches in synthetic_heldout(200).items():
        began = time.time()
        rows = run_baseline(benches, budget, 120.0, workers=6)
        save(f"ceiling_synthetic-tier{tier}_brute_force_{budget}", rows,
             {"suite": f"synthetic-tier{tier}", "solver": f"brute force ({budget} calls)"})
        s = summary(rows)
        print(f"tier {tier}: {s['solved']}/{s['problems']} ({100 * s['rate']:.1f}%), "
              f"mean calls when solved {s['mean_calls_solved']}, {time.time() - began:.0f}s", flush=True)
