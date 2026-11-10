"""Run the brute-force baseline on the seed and real benchmarks and save results/baseline_*.json.

    .venv/bin/python scripts/run_baseline.py                       # 20,000 calls, 60 s per problem, both suites
    .venv/bin/python scripts/run_baseline.py 20000 120 widening v1 --suite real

The optional label goes into the file name, so that a later code version does
not overwrite an earlier record.
"""
import argparse
import time

from alphafe.baseline.guesser import guess
from alphafe.bench import load_real, load_seed
from alphafe.eval import markdown_by_mohs, markdown_summary, run_baseline, save, unflagged

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Brute-force baseline on the seed and real benchmarks.")
    parser.add_argument("max_calls", nargs="?", type=int, default=20000, help="checker calls per problem")
    parser.add_argument("max_seconds", nargs="?", type=float, default=60.0, help="time limit per problem")
    parser.add_argument("mode", nargs="?", choices=("widening", "plain"), default="widening",
                        help="widening pool ladder (default) or one breadth-first search over the full pool")
    parser.add_argument("label", nargs="?", default="", help="suffix for the result file names")
    parser.add_argument("--suite", action="append", choices=("seed", "real"), help="repeatable; default: both")
    args = parser.parse_args()
    widening = args.mode == "widening"
    tag = ("" if widening else "_plainbfs") + (f"_{args.label}" if args.label else "")
    loaders = {"seed": load_seed, "real": load_real}
    for name in args.suite or ("seed", "real"):
        benches = loaders[name]()
        if not benches:
            print(f"{name}: no problems")
            continue
        began = time.time()
        rows = run_baseline(benches, args.max_calls, args.max_seconds, widening=widening)
        save(f"baseline_{name}_{args.max_calls}{tag}", rows,
             {"suite": name, "solver": "brute force", "max_calls": args.max_calls, "max_seconds": args.max_seconds,
              "widening": widening})
        print(f"== {name}: brute force, budget {args.max_calls} checker calls, {time.time() - began:.0f}s wall")
        print(markdown_summary({"brute force": rows}))
        print(markdown_by_mohs({"brute force": rows}))
        if any(r.flags for r in rows):
            clean = unflagged(rows)
            print(f"without the {len(rows) - len(clean)} flagged problems:")
            print(markdown_summary({"brute force": clean}))
            print(markdown_by_mohs({"brute force": clean}))
        for r in rows:
            print(f"  {r.id} {'solved' if r.solved else 'FAILED'} calls={r.checker_calls} {r.equation}  {r.answer or r.reason}")
        guesses = {b.id: guess(b.problem) for b in benches}
        right = sum(1 for b in benches if guesses[b.id].solutions == b.expected)
        print(f"guesser: answer matches the recorded one on {right}/{len(benches)}")
        for b in benches:
            if guesses[b.id].solutions != b.expected:
                print(f"  guesser differs on {b.id}: {b.problem.equation}: guessed {guesses[b.id]}, expected {b.expected}")
