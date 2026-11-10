"""Check benchmark files before committing them.

    .venv/bin/python scripts/validate_bench.py                     # every *.jsonl in benchmarks/real
    .venv/bin/python scripts/validate_bench.py path/to/file.jsonl  # specific files
    .venv/bin/python scripts/validate_bench.py --seed              # the seed benchmark (fewer required fields)

Exits with status 1 if there is any error. See benchmarks/real/INSTRUCTIONS.md
for what each message means and alphafe/benchcheck.py for what is checked.
"""
import argparse
import sys

from alphafe.bench import BENCH_DIR
from alphafe.benchcheck import in_training_pool, validate

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check benchmark files.")
    parser.add_argument("paths", nargs="*", help="JSON Lines files (default: benchmarks/real/*.jsonl)")
    parser.add_argument("--seed", action="store_true", help="check benchmarks/seed with the basic field list")
    parser.add_argument("--no-training-check", action="store_true",
                        help="skip the comparison with the synthetic training pool (about 10 seconds)")
    args = parser.parse_args()

    strict = not args.seed
    paths = args.paths or sorted((BENCH_DIR / ("seed" if args.seed else "real")).glob("*.jsonl"))
    if not paths:
        print("no .jsonl files to check")
        sys.exit(0)

    report = validate(paths, strict=strict)
    for message in report.warnings:
        print("warning:", message)
    for message in report.errors:
        print("ERROR:  ", message)

    if strict and report.ok and not args.no_training_check:
        seen = in_training_pool(paths)
        if seen:
            print(f"note: {len(seen)} problem(s) are also produced by the synthetic training generator, so the "
                  f"checkpoints published before this file existed may have trained on them: {', '.join(seen)}")
            print('      keep them, add "in_training_pool": true to each, and say so when reporting results')

    print(f"{report.records} record(s), {len(report.errors)} error(s), {len(report.warnings)} warning(s)")
    sys.exit(0 if report.ok else 1)
