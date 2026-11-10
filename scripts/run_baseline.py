"""Run the baselines on the seed (and real) benchmarks and save results/baseline_*.json."""
import sys
import time

from alphafe.baseline.guesser import guess
from alphafe.bench import load_real, load_seed
from alphafe.eval import markdown_by_mohs, markdown_summary, run_baseline, save

if __name__ == "__main__":
    max_calls = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    max_seconds = float(sys.argv[2]) if len(sys.argv) > 2 else 60.0
    widening = (sys.argv[3] if len(sys.argv) > 3 else "widening") == "widening"
    tag = "" if widening else "_plainbfs"
    for name, benches in (("seed", load_seed()), ("real", load_real())):
        if not benches:
            print(f"{name}: no problems")
            continue
        began = time.time()
        rows = run_baseline(benches, max_calls, max_seconds, widening=widening)
        save(f"baseline_{name}_{max_calls}{tag}", rows,
             {"solver": "brute force", "max_calls": max_calls, "max_seconds": max_seconds, "widening": widening})
        print(f"== {name}: brute force, budget {max_calls} checker calls, {time.time() - began:.0f}s wall")
        print(markdown_summary({"brute force": rows}))
        print(markdown_by_mohs({"brute force": rows}))
        for r in rows:
            print(f"  {r.id} {'solved' if r.solved else 'FAILED'} calls={r.checker_calls} {r.equation}  {r.answer or r.reason}")
        right = sum(1 for b in benches if guess(b.problem).solutions == b.expected)
        print(f"guesser: answer matches the recorded one on {right}/{len(benches)}")
        for b in benches:
            g = guess(b.problem)
            if g.solutions != b.expected:
                print(f"  guesser differs on {b.id}: {b.problem.equation}: guessed {g}, expected {b.expected}")
