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

- **M5** and **M6 experiments E1-E7**: see RESULTS.md (E1-E4 helped; E5 subterm
  exploration, E6 longer training and E7 value-guided search did not). Search now commits when a
  case closes; proposals are sampled at a spread of temperatures; training
  minimises proofs and mirrors them (x <-> y); the held-out set is frozen in
  `benchmarks/synthetic/heldout.jsonl`; seeds s47-s50 are three-variable.

## Next

See the end of RESULTS.md for the current failure analysis. Open directions,
most promising first:

1. The unsolved 10M seeds (s37, s38, s42, s46, s43) each hinge on one "idea"
   substitution the network gives almost no probability (`scripts/diagnose.py`
   shows which). More self-play at larger budgets on tiers 3-4, or a generator
   that produces more problems needing such substitutions, is the next thing to try.
2. Give the generator three-variable problems.
3. Product reasoning in the checker (multiply an identity by a term and reduce
   products) and wider injectivity/surjectivity criteria.
4. More training seeds and sampling seeds, to turn "within noise" into answers.

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
.venv/bin/python scripts/diagnose.py checkpoints/NAME/last.pt [ids]   # probability the network gives each hand-proof move
.venv/bin/python scripts/freeze_heldout.py           # (re)write benchmarks/synthetic/heldout.jsonl; do not rerun casually
```

## State of the local (uncommitted) artefacts

- `checkpoints/v1/m5.pt` (M5), `checkpoints/v2/e4.pt` (28 min), `checkpoints/v2/e6.pt`
  (56 min, also copied to `checkpoints/best.pt`, which `alphafe solve` loads),
  `checkpoints/v3/e5.pt` (subterm exploration). None are in git; weights-only copies of the two v2 files are on the v0.1.0 GitHub release. Otherwise retrain with
  `alphafe train` if they are gone.
- `logs/` has the raw training logs; compact copies are in `results/train_*_log.json`.

## Known problems

- MPS (Apple GPU) memory grows if tensor shapes are not bucketed; see DECISIONS.md.
- Training runs are capped at about 28 minutes per invocation; use `--resume` to continue.
- Checkpoints, logs and `.worktrees/` are not committed. `checkpoints/best.pt` is what
  `alphafe solve` loads; copy a run's `last.pt` there.
