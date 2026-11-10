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

- **M4 code**: `alphafe/generate.py` (synthetic problems, tiers, train/held-out
  split), `alphafe/tokenizer.py` (state/move tokens, `MoveGrammar`),
  `alphafe/search.py` (greedy and best-first search, uniform reference policy),
  `alphafe/model.py` (2.5M-parameter transformer, `NeuralProposer`),
  `alphafe/train.py` (self-play loop, replay buffer, curriculum, resume),
  `alphafe/eval.py` (three-mode evaluation), `alphafe/cli.py`.
- **Checker extensions (first M6 language fix)**: polynomial Cauchy and the
  quadratic lemma over Q, unique-root deduction (`tests/test_lemmas.py`).

## Next

See the end of RESULTS.md for the current failure analysis and the list of
experiments tried. Open directions, most promising first:

1. More self-play at larger budgets on tiers 3-4 (the network's weak spot).
2. Product reasoning in the checker (multiply an identity by a term and reduce
   products), needed for s36 `f(x-y) = f(x)f(y)`.
3. Wider injectivity/surjectivity criteria.

## How to run

```sh
.venv/bin/python -m pytest          # all tests
.venv/bin/python scripts/check_seed_proofs.py     # hand-written seed proofs
.venv/bin/python scripts/play.py "f(x+y) = f(x) + y" R proof.txt   # replay a proof step by step
.venv/bin/python scripts/fuzz.py 40 80            # long soundness fuzz
.venv/bin/python scripts/run_baseline.py 20000 120   # baseline on seed (+ real) benchmarks
.venv/bin/alphafe train --run NAME --minutes 28 [--resume]   # self-play training
.venv/bin/python scripts/show_log.py NAME            # summarise logs/NAME/train.jsonl
.venv/bin/alphafe eval --checkpoint checkpoints/NAME/last.pt --tag NAME   # three-mode evaluation
.venv/bin/python scripts/analyse_failures.py results/FILE.json   # sort seed failures into groups
```

## Known problems

- MPS (Apple GPU) memory grows if tensor shapes are not bucketed; see DECISIONS.md.
- Training runs are capped at about 28 minutes per invocation; use `--resume` to continue.
- Checkpoints, logs and `.worktrees/` are not committed. `checkpoints/best.pt` is what
  `alphafe solve` loads; copy a run's `last.pt` there.
