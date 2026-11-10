# Progress

A fresh session should read this file, `DECISIONS.md` and `git log` first.

## Done

- **M0 scaffold**: `pyproject.toml`, package `alphafe/`, pytest, `.gitignore`, docs.
- **M1 terms and algebra**: `alphafe/terms.py` (expression trees, infix parser and
  printer, prefix serialisation) and `alphafe/algebra.py` (canonical polynomials,
  substitution, deep rewriting, exact division, rational roots, factoring hints,
  evaluation). Property tests and a SymPy cross-check in `tests/`.

- **M2 checker, moves, renderer**: `alphafe/checker.py` (trusted core: branches,
  automatic normalisation, 11 moves, `check`), `alphafe/moves.py` (move data +
  text format), `alphafe/solutions.py` (families, exact parameter solver,
  canonical solution sets, verification), `alphafe/render.py` (AoPS-style
  write-up), `alphafe/modelcheck.py` (soundness fuzzing tool).
  - `benchmarks/seed/seed.jsonl`: 46 seed problems with expected answers.
  - `benchmarks/seed/proofs/*.proof`: 32 hand-written proofs, all checked.
  - `tests/test_traps.py`: wrong proofs for every soundness trap, all rejected.
  - `tests/test_modelcheck.py` + `scripts/fuzz.py`: random moves vs known solutions.

- **M3 baselines**: `alphafe/env.py` (search environment: free moves applied
  after each proposed move, `SearchResult`, `confirm`), `alphafe/baseline/`
  (guesser, brute force with iterative widening), `alphafe/bench.py` (benchmark
  loading + answer canary), `alphafe/eval.py` (scoring, tables, `results/*.json`).
  Seed solve rates are in RESULTS.md (37/46 at 20,000 checker calls).

## Next

- M4 generator/tokenizer/model/training; M5; M6.

## How to run

```sh
.venv/bin/python -m pytest          # all tests
.venv/bin/python scripts/check_seed_proofs.py     # hand-written seed proofs
.venv/bin/python scripts/play.py "f(x+y) = f(x) + y" R proof.txt   # replay a proof step by step
.venv/bin/python scripts/fuzz.py 40 80            # long soundness fuzz
.venv/bin/python scripts/run_baseline.py 20000 120   # baseline on seed (+ real) benchmarks
```

## Known problems

- None yet.
