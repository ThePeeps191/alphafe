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

- **M9 saturation and speed**: `benchmarks/dev` (a development suite of 32
  harder problems, `--suite dev`); the checker about five times faster with
  identical results (`algebra.FAtom`, cached leading monomials, memoised
  routine instances, work limits); `model.StepDecoder`; searches take two of
  eight proposals per state from the page; opening substitutions at 1, -1 and
  f of a variable, with 80 identities per case; `cancel` on constant
  arguments; tests against non-polynomial solutions (`tests/test_nonpoly.py`);
  training with self-play workers, an adaptive curriculum and a step cap.
  Numbers are in RESULTS.md, M9.

- **M9 real benchmark and v0.3.0**: third run of the real benchmark, 45 of
  the 124 unseen problems at 2,000 calls against 43 in M8. The rows without
  a trained network roughly doubled at small budgets, and the m3 weights
  (150 minutes) are not measurably better than random weights on real
  problems. Four problems solved in M8 are lost (#110).

## Next

The task list is the GitHub issue tracker; issue #99 is the roadmap and its
comments record what is done. The rule for every milestone: choose the
configuration on the seed and held-out sets only, then run the real
benchmark once, under a protocol committed before the run (RESULTS.md, M7 to
M9, show the form). Most promising next, in order:

1. Training (#107). The trained weights do no better than random ones on
   real problems. Self-play problems are mostly solved by the routine moves,
   so the trainer sees few proofs with several proposed moves, and the
   network reads 14 of a median 25 identities. In progress on the local
   branch `work`: problems hidden behind changes of variables whose proofs
   are known by construction (`alphafe/planted.py`, #83), and an encoder
   that reads every identity (#108, #16). The comparison that decides is
   trained against random weights on a held-out set sorted by proof length.
2. The four real problems lost since M8 (#110) and searches that stop with
   an empty frontier (#111).
3. Shifted instances such as f(x - 2) are what the routine moves still
   refuse; a plain cap on them feeds itself (#106).
4. A proposed move costs about three times more in the larger states (#109).
5. More moves for 15M to 20M problems: #77 and #78, then #80 and #81.

Nothing heavy may run on the machine while a training run is going: a run is
limited by wall-clock time (DECISIONS.md).

## How to run

```sh
.venv/bin/python -m pytest          # all tests
.venv/bin/python scripts/check_seed_proofs.py     # hand-written seed proofs
.venv/bin/python scripts/play.py "f(x+y) = f(x) + y" R proof.txt   # replay a proof step by step
.venv/bin/python scripts/fuzz.py 40 80            # long soundness fuzz
.venv/bin/python scripts/run_baseline.py 20000 120 [--suite real]   # brute force on the seed and real benchmarks
.venv/bin/alphafe train --run NAME --minutes 28 [--resume]   # self-play training
.venv/bin/alphafe train --run NAME --minutes 150 --set workers=6 --set curriculum=adaptive --set n_subterm=2   # as run m3
.venv/bin/alphafe eval --suite dev --checkpoint checkpoints/best.pt --big-budget 2000   # the development suite
.venv/bin/python scripts/ablate_routine.py full 2000 600 out.json   # brute force under one environment configuration
.venv/bin/python scripts/show_log.py NAME            # summarise logs/NAME/train.jsonl
.venv/bin/alphafe eval --checkpoint checkpoints/NAME/last.pt --tag NAME [--suite seed]   # three-mode evaluation
.venv/bin/python scripts/analyse_failures.py results/FILE.json   # sort seed failures into groups
.venv/bin/python scripts/diagnose.py checkpoints/NAME/last.pt [--suite dev] [ids]   # probability the network gives each hand-proof move
.venv/bin/python scripts/freeze_heldout.py --check   # compare a fresh generation with the frozen file (--force overwrites)
```

## State of the local (uncommitted) artefacts

- `checkpoints/alphafe-m3-150min.pt` (M9, release v0.3.0; also copied to `checkpoints/best.pt`, which
  `alphafe solve` loads) and the full training state in `checkpoints/m3/`. `checkpoints/alphafe-m1-56min.pt`
  (M8, release v0.2.0) and `checkpoints/m1/`. Older: `checkpoints/v1/m5.pt` (M5),
  `checkpoints/v2/e4.pt` and `e6.pt` (version 1, on the v0.1.0 release), `checkpoints/v3/e5.pt`. None are in
  git. Retrain with `alphafe train` if they are gone.
- `logs/` has the raw training logs; compact copies are in `results/train_*_log.json`.

## Known problems

- MPS (Apple GPU) memory grows if tensor shapes are not bucketed; see DECISIONS.md.
- Training runs are capped at about 28 minutes per invocation; use `--resume` to continue.
- Seed problems s02 and s38 are s01 and s37 with x and y exchanged (found by `scripts/validate_bench.py --seed`), so the seed set has 48 distinct problems. They are kept so that earlier results stay comparable.
- Checkpoints, logs and `.worktrees/` are not committed. `checkpoints/best.pt` is what
  `alphafe solve` loads; copy a run's `last.pt` there.
