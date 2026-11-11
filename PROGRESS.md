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

- **M7 real benchmark**: `benchmarks/real/` (137 competition problems selected by
  rules fixed in advance, 13 flagged as not fully unseen), the validator
  (`alphafe/benchcheck.py`, `scripts/validate_bench.py`) and the version 1
  baseline: 13 of the 124 unflagged problems at 2,000 calls.
- **M8 routine moves**: `env.close` applies opening substitutions, the swap,
  closed instances and witnesses by itself; `env.prune` and `env.minimise` cut
  found proofs back to the moves they use; depth limit 16 per case; lemmas
  `sqadd` and `sqlin`; USAMO 2002/4 added as seed s51; training pool excludes
  twins of benchmark problems and problems the environment solves alone;
  network retrained (`m1`, release v0.2.0). Real benchmark: 43 of 124.
- **Harness and hygiene**: `alphafe eval --suite`, provenance in result files,
  answer mismatches kept with their proof, CI on Python 3.11 to 3.13,
  checkpoints record their vocabulary, safe `train --resume`, one-line CLI
  errors, every script has `--help`.

## Next

The task list is the GitHub issue tracker; issue #99 is the roadmap and its
comments record what is done. The rule for every milestone: choose the
configuration on the seed and held-out sets only, then run the real
benchmark once, under a protocol committed before the run (RESULTS.md, M7 and
M8, show the form). Most promising next, in order:

1. The network gives some single "idea" moves no probability (`y := f(y)`),
   so it misses one-move proofs that brute force finds: issues #105 (search),
   #92 and #83 (training data), #103 (the curriculum no longer runs easy to
   hard).
2. Speed: a checker call is several times slower with the routine moves, and
   half of a long evaluation is garbage collection (#104).
3. More moves for 15M to 20M problems: #77 and #78 (IMO 1999/6), then the
   small checker deductions #79 to #81.
4. Several training seeds, so that single-run differences can be trusted.

After M8 the seed problems the network misses at 2,000 calls are s37, s38,
s39, s42 and s46; brute force misses s33, s34 and s46.

## How to run

```sh
.venv/bin/python -m pytest          # all tests
.venv/bin/python scripts/check_seed_proofs.py     # hand-written seed proofs
.venv/bin/python scripts/play.py "f(x+y) = f(x) + y" R proof.txt   # replay a proof step by step
.venv/bin/python scripts/fuzz.py 40 80            # long soundness fuzz
.venv/bin/python scripts/run_baseline.py 20000 120 [--suite real]   # brute force on the seed and real benchmarks
.venv/bin/alphafe train --run NAME --minutes 28 [--resume]   # self-play training
.venv/bin/python scripts/show_log.py NAME            # summarise logs/NAME/train.jsonl
.venv/bin/alphafe eval --checkpoint checkpoints/NAME/last.pt --tag NAME [--suite seed]   # three-mode evaluation
.venv/bin/python scripts/analyse_failures.py results/FILE.json   # sort seed failures into groups
.venv/bin/python scripts/diagnose.py checkpoints/NAME/last.pt [ids]   # probability the network gives each hand-proof move
.venv/bin/python scripts/freeze_heldout.py --check   # compare a fresh generation with the frozen file (--force overwrites)
```

## State of the local (uncommitted) artefacts

- `checkpoints/alphafe-m1-56min.pt` (M8, release v0.2.0; also copied to `checkpoints/best.pt`, which
  `alphafe solve` loads) and the full training state in `checkpoints/m1/`. Older: `checkpoints/v1/m5.pt` (M5),
  `checkpoints/v2/e4.pt` and `e6.pt` (version 1, on the v0.1.0 release), `checkpoints/v3/e5.pt`. None are in
  git. Retrain with `alphafe train` if they are gone.
- `logs/` has the raw training logs; compact copies are in `results/train_*_log.json`.

## Known problems

- MPS (Apple GPU) memory grows if tensor shapes are not bucketed; see DECISIONS.md.
- Training runs are capped at about 28 minutes per invocation; use `--resume` to continue.
- Seed problems s02 and s38 are s01 and s37 with x and y exchanged (found by `scripts/validate_bench.py --seed`), so the seed set has 48 distinct problems. They are kept so that earlier results stay comparable.
- Checkpoints, logs and `.worktrees/` are not committed. `checkpoints/best.pt` is what
  `alphafe solve` loads; copy a run's `last.pt` there.
