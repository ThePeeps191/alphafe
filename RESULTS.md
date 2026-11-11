# Results

Every number here was produced by the code in this repository. Each run is
saved under `results/` (JSON, one row per problem, with the found proof).
Negative results stay in.

**Definitions.** "Solved" means a complete proof was found *and* re-checked
from scratch by `checker.check`; if a recorded answer exists, the proof's
solution set must equal it (a mismatch aborts the run instead of being
scored). "Checker calls" counts proposed moves sent to the checker, accepted
or not; the free moves applied automatically after each proposal (conclude,
cauchy, inj, surj, cancel) are not counted. "Time" is wall-clock seconds per
problem, solved or not. Brute force runs 8 problems in parallel on CPU
cores; the network modes run all problems of a suite together in one process
with batched GPU calls, and their time is the suite's total divided by the
number of problems. Other jobs often shared the machine, so read times as
rough.

**Reproducing a row.** Rows that sample from a network (trained or
untrained) depend on the device as well as on the seed: the same seed gives
the same rows on the Apple GPU every time, and different rows on the CPU
(the untrained-network seed rows are 25 and 32 solved on the GPU, as
recorded, and 29 and 31 on the CPU). Brute-force and uniform-policy rows are
the same everywhere. A row also depends on which problems share its suite,
because the searches of a suite draw from one random stream (issue #100).
Result files written from M7 on record the commit, the device, the hash of
the weights and the settings; earlier files do not.

## M3: baselines on the seed benchmark (46 problems)

Hardware: Apple M6, 12 cores, CPU only. Command: `python scripts/run_baseline.py <calls> 120`.

### Brute force

Breadth-first search over a fixed pool of substitution terms (28 single
terms, 15 terms for double substitutions), case splits, preimages, with
duplicate-state merging. "Widening" searches a 5-term pool deeply first, then
a 15-term pool, then the full pool.

| solver | budget (checker calls) | solved | 0M | 5M | 10M | 15M | 20M | mean calls when solved |
|---|---|---|---|---|---|---|---|---|
| brute force, widening | 200 | 26/46 (56.5%) | 20/20 | 5/13 | 1/11 | 0/1 | 0/1 | 8.7 |
| brute force, widening | 2,000 | 33/46 (71.7%) | 20/20 | 10/13 | 3/11 | 0/1 | 0/1 | 154.4 |
| brute force, widening | 20,000 | 37/46 (80.4%) | 20/20 | 12/13 | 5/11 | 0/1 | 0/1 | 1100.0 |
| brute force, plain BFS | 20,000 | 33/46 (71.7%) | 20/20 | 8/13 | 5/11 | 0/1 | 0/1 | 718.4 |
| brute force, plain BFS | 50,000 | 35/46 (76.1%) | 20/20 | 8/13 | 7/11 | 0/1 | 0/1 | 2531.9 |

Time per problem: 0.02 s at 200 calls, 0.16 s at 2,000, 1.3 s at 20,000
(widening); plain BFS 1.9 s at 20,000 and 4.0 s at 50,000. On problems that
exhaust their budget the checker handles a few thousand proposed moves per
second on one core (about 5,000 on the seed problems).

Unsolved by widening brute force at 20,000 calls: s33, s34 (two nested case
splits), s36, s37, s38, s42, s44, s45, s46.

### Answer guesser

Plugging in `ax^2 + bx + c` and solving for the coefficients gives the
recorded answer on 45/46 seed problems. The miss is s31, whose answer
`x^3 + cx` is not quadratic. The guesser produces answers only, never proofs
that nothing else works.

### Reading

* The checker's automatic normalisation does a lot: every 0M seed problem
  falls to one or two substitutions, so brute force is a strong control at
  the easy end. A network can only beat it on *cost* there (fewer checker
  calls), not on solve rate.
* The room for a learned policy is at 5-10M, where brute force needs
  thousands of calls or fails: proofs needing a specific double substitution,
  a substitution into a derived identity, or two case splits.
* No accepted proof gave an answer different from the recorded one.

## M4: first self-play training run (run `v1`)

Setup: 2.5M-parameter encoder-decoder transformer, random initialisation,
Apple M6 GPU (MPS). Synthetic problems: 3,000 generated per tier, about 2,700
train / 300 held out per tier (split by canonical hash; seed problems
excluded). Self-play: 192 problems per iteration, best-first search with 48
checker calls, 8 proposals per state of which 2 uniform-random; 60 gradient
steps of batch 128 per iteration. Curriculum: move up a tier when the
self-play solve rate on the current tier reaches 0.75, or after 25 iterations.
One run, 28 minutes, 76 iterations, code at commit `414fae4`
(`alphafe train --run v1 --minutes 28`). Log: `results/train_v1_log.json`.

Held-out solve rate during training (100 held-out problems per tier, network
without backtracking, 32 checker calls):

| iteration | training tier | tier 1 | tier 2 | tier 3 | tier 4 |
|---|---|---|---|---|---|
| uniform-random policy (reference) | - | 0.57 | 0.35 | | |
| 10 | 2 | 0.79 | 0.58 | | |
| 20 | 2 | 0.84 | 0.65 | | |
| 30 | 2 | 0.82 | 0.68 | | |
| 40 | 3 | 0.83 | 0.61 | 0.34 | |
| 50 | 3 | 0.86 | 0.66 | 0.34 | |
| 60 | 4 | 0.84 | 0.65 | 0.36 | 0.12 |
| 70 | 4 | 0.89 | 0.69 | 0.37 | 0.11 |

**M4 acceptance** (easiest tier, 200 held-out problems, no backtracking, 32
calls; from the M5 evaluation below): trained network 171/200 (85.5%, mean
1.5 calls when solved) against 153/200 (76.5%, 4.3 calls) for the same
architecture with random weights and 112/200 (56.0%, 9.3 calls) for the
uniform grammar policy. The margin over the untrained network is modest on
tier 1 because tier 1 is easy enough that random proposals solve most of it
within 32 calls; on tier 2 it is 70.0% against 53.0%.

## M5: curriculum through tier 4 and the three-mode evaluation

Checkpoint: run `v1` after 28 minutes. Code pinned at commit `28a26e5`.
Command: `alphafe eval --checkpoint checkpoints/v1/m5.pt --tag m5`.
Raw rows: `results/m5_*.json`, tables: `results/m5.md`.

Modes: **no backtracking** = commit to the most probable sampled proposal the
checker accepts, at most 32 checker calls; **search** = best-first on move
log-probability, at most 128 calls; **brute force** = the M3 baseline at 128
and at 2,000 calls. "Untrained network" is the same architecture with random
weights; "uniform policy" picks every grammar-allowed token with equal probability.

### Held-out synthetic problems (200 per tier; answers unknown, so "solved" = checked proof found)

| solver | tier 1 | tier 2 | tier 3 | tier 4 |
|---|---|---|---|---|
| network, no backtracking (32 calls) | **85.5%** | **70.0%** | **31.5%** | 16.0% |
| untrained network, no backtracking (32) | 76.5% | 53.0% | 21.5% | 15.0% |
| uniform policy, no backtracking (32) | 56.0% | 33.0% | 11.5% | 11.0% |
| network, search (128 calls) | **91.0%** | **80.5%** | 36.5% | 25.5% |
| untrained network, search (128) | 83.5% | 64.5% | 32.0% | 21.0% |
| uniform policy, search (128) | 81.0% | 63.0% | 27.5% | 18.5% |
| brute force (128 calls) | 86.0% | 66.0% | 30.0% | 23.0% |
| brute force (2,000 calls) | 88.0% | 71.5% | **40.0%** | **26.0%** |

Mean checker calls on solved problems, tier 1 to tier 4: network without
backtracking 1.5 / 1.8 / 1.7 / 2.1; network search 3.6 / 7.1 / 8.9 / 9.2;
brute force (128) 4.1 / 4.0 / 7.3 / 13.3; brute force (2,000) 36.5 / 45.2 / 80.8 / 37.3.

### Seed benchmark (46 problems)

| solver | solved | 0M | 5M | 10M | 15M | 20M | mean calls when solved |
|---|---|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 20/46 (43.5%) | 15/20 | 5/13 | 0/11 | 0/1 | 0/1 | 1.2 |
| untrained network, no backtracking (32) | 24/46 (52.2%) | 16/20 | 8/13 | 0/11 | 0/1 | 0/1 | 6.6 |
| uniform policy, no backtracking (32) | 15/46 (32.6%) | 9/20 | 6/13 | 0/11 | 0/1 | 0/1 | 10.3 |
| network, search (128 calls) | 27/46 (58.7%) | 18/20 | 9/13 | 0/11 | 0/1 | 0/1 | 11.7 |
| untrained network, search (128) | 27/46 (58.7%) | 19/20 | 7/13 | 1/11 | 0/1 | 0/1 | 12.3 |
| uniform policy, search (128) | 26/46 (56.5%) | 18/20 | 7/13 | 1/11 | 0/1 | 0/1 | 21.8 |
| brute force (128 calls) | 26/46 (56.5%) | 20/20 | 5/13 | 1/11 | 0/1 | 0/1 | 7.2 |
| brute force (2,000 calls) | 33/46 (71.7%) | 20/20 | 10/13 | 3/11 | 0/1 | 0/1 | 154.4 |

The real benchmark did not exist when these runs were made. It now holds 137
problems (`benchmarks/real/`); the first run on it is M7 below.

Time per problem in seconds (M5 run):

| solver | seed | tier 1 | tier 2 | tier 3 | tier 4 |
|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 0.013 | 0.010 | 0.021 | 0.024 | 0.036 |
| network, search (128 calls) | 0.084 | 0.027 | 0.098 | 0.242 | 0.400 |
| untrained network, no backtracking (32) | 0.076 | 0.041 | 0.111 | 0.182 | 0.211 |
| untrained network, search (128) | 0.095 | 0.047 | 0.125 | 0.207 | 0.262 |
| uniform policy, no backtracking (32) | 0.004 | 0.002 | 0.004 | 0.006 | 0.008 |
| uniform policy, search (128) | 0.009 | 0.005 | 0.010 | 0.021 | 0.028 |
| brute force (128 calls) | 0.014 | 0.005 | 0.014 | 0.036 | 0.047 |
| brute force (2,000 calls) | 0.159 | 0.055 | 0.189 | 0.526 | 0.754 |

In wall-clock time the network is *not* cheaper than brute force at the same
number of checker calls: a checker call costs a fraction of a millisecond and
a batch of network proposals costs far more. The network saves checker calls, not
seconds, at this problem size.

### Plain reading

1. **On problems like its training data, the network learned something real.**
   On every held-out tier it solves more than the untrained network and the
   uniform policy, and it needs about one checker call where they need 4-10.
   With 128 calls it is ahead of brute force at the same budget on all four
   tiers; the margin is clear on tier 2 (80.5% vs 66.0%) and within noise on
   the others (these are single sampling runs on 200 problems, so differences
   under about 7 points are not meaningful).
2. **It does not beat brute force everywhere.** Brute force with 2,000 calls
   is level with the network at 128 calls on tiers 3 and 4 (40.0% vs 36.5%,
   26.0% vs 25.5%).
3. **On the seed benchmark, training did not help, and without backtracking it
   hurt.** Search: 27/46 trained, 27/46 untrained. No backtracking: 20/46
   trained against 24/46 untrained. Brute force with 2,000 calls solves 33/46.
   The trained network fails even s01, `f(x+y) = f(x) + y`.
4. **Why (diagnosed after the run).** The policy collapsed onto a favourite
   move: in most start states it gives `sub R1: y:=0` a probability of about
   1. All eight samples are then the same move, and when the checker rejects
   it there is nothing else to try. On synthetic problems that habit pays off
   often enough; on seed problems, many of which need `x:=0` or a double
   substitution, it does not. The untrained network does better without
   backtracking simply because its eight samples are different.
5. One thing the network did that we had not: it proved s36,
   `f(x-y) = f(x)f(y)`, which we had filed under "the move language cannot
   express this" (`benchmarks/seed/proofs/s36.proof`).

### Failure analysis after M5 (seed benchmark, network search, 19 unsolved)

| group | count | problems |
|---|---|---|
| the language cannot express the proof | 2 | s44 (Cauchy with a polynomial term), s45 (quadratic equation) |
| the proof is too deep (5+ creative moves in the shortest known proof) | 2 | s33, s34 |
| the network did not find it (a proof of 1-4 creative moves is known) | 15 | s18, s20, s24, s25, s29, s31, s35, s37, s38, s39, s40, s41, s42, s43, s46 |

The largest group is "the network did not find it", and six of those fifteen
need a single substitution. That points at the proposal collapse, not at
depth or expressiveness, so it is what M6 attacks first.

## M6: experiments after the first failure analysis

Each experiment lists what changed, the commit, and what happened. E1-E3 use
the same seed benchmark (46 problems) and exactly the same held-out synthetic
problems (200 per tier) as M5; the held-out list is now frozen in
`benchmarks/synthetic/heldout.jsonl` (verified identical to the problems
evaluated in M5 and E2).

**Caveats that apply to everything below.**

* *The seed benchmark has become a development set.* The lemmas, the
  temperature spread and the case commit were all chosen by looking at seed
  failures. Seed numbers from here on show whether a fix did what it was meant
  to do; they are not an unbiased estimate of anything. The held-out synthetic
  set was not used to design E1-E4, but it was used to compare runs: the
  decisions to leave E5 and E7 switched off, and the choice of which
  checkpoint to keep, looked at it. The real benchmark is the only untouched
  one, apart from the 13 problems it flags as seen in development or in the
  training pool.
* *Noise.* Network rows up to and including E2 are a single sampling run, and
  each training configuration was run with one seed. On 200 problems a
  difference of fewer than about 14 problems (7 points) between two solvers is
  within what one would expect from chance alone; on the seed set, about 3
  problems. E4 reports ranges over sampling seeds.

### E1. Language: lemmas over Q and unique roots (commit `49e942d`)

Change: `cauchy` accepts a polynomial defect (`f(x+y) = f(x) + f(y) + 2xy`),
new free move `quadratic` (`f(x+y) + f(x-y) = 2f(x) + 2f(y)`), and an
equation in one unknown quantity with exactly one root in the domain yields
that root. This addresses the "language cannot express" group (s44, s45).

Brute force on seeds, before -> after: 200 calls 26 -> 28; 2,000 calls 33 -> 35;
20,000 calls 37 -> 39 (`results/baseline_seed_*_lemmas.json`). s44 and s45
are now solved by the free moves alone, for every solver.

### E2. Proposal diversity, no retraining (v1 weights; commits `827949f`, evaluated at `a7d21de`; `results/m6a_*`)

Change: the eight proposals for a state are sampled at a spread of
temperatures (0.6 to 3.0) instead of one, and ranked by the model's own
probability. Same weights as M5. (This evaluation also contains E1, which
adds s44 and s45 to every solver's count.)

Seed benchmark:

| solver | M5 | E2 | 0M | 5M | 10M | 15M | 20M | mean calls when solved |
|---|---|---|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 20/46 | **28/46** | 19/20 | 7/13 | 1/11 | 1/1 | 0/1 | 2.1 |
| untrained network, no backtracking (32) | 24/46 | 22/46 | 14/20 | 6/13 | 1/11 | 1/1 | 0/1 | 5.4 |
| uniform policy, no backtracking (32) | 15/46 | 18/46 | 11/20 | 5/13 | 1/11 | 1/1 | 0/1 | 7.6 |
| network, search (128 calls) | 27/46 | **32/46** | 19/20 | 11/13 | 1/11 | 1/1 | 0/1 | 7.4 |
| untrained network, search (128) | 27/46 | 28/46 | 19/20 | 7/13 | 1/11 | 1/1 | 0/1 | 15.7 |
| uniform policy, search (128) | 26/46 | 28/46 | 18/20 | 7/13 | 2/11 | 1/1 | 0/1 | 19.0 |
| brute force (128 calls) | 26/46 | 28/46 | 20/20 | 5/13 | 2/11 | 1/1 | 0/1 | 6.6 |
| network, search (2,000 calls) | - | **37/46** | 20/20 | 13/13 | 3/11 | 1/1 | 0/1 | 80.0 |
| brute force (2,000 calls) | 33/46 | 35/46 | 20/20 | 10/13 | 4/11 | 1/1 | 0/1 | 145.6 |

Held-out synthetic problems (M5 value in brackets):

| solver | tier 1 | tier 2 | tier 3 | tier 4 |
|---|---|---|---|---|
| network, no backtracking (32 calls) | 88.0% (85.5) | 78.5% (70.0) | 34.0% (31.5) | 21.5% (16.0) |
| network, search (128 calls) | 91.0% (91.0) | 81.5% (80.5) | 38.5% (36.5) | 27.0% (25.5) |
| untrained network, no backtracking (32) | 68.0% | 51.0% | 21.5% | 14.0% |
| untrained network, search (128) | 83.0% | 65.5% | 32.5% | 19.0% |
| brute force (128 calls) | 86.5% | 66.0% | 30.0% | 23.0% |
| brute force (2,000 calls) | 88.5% | 72.0% | 40.5% | 26.0% |

Provenance note: this evaluation was started at commit `a7d21de`, and the case
commit of E3 was written to disk while it was running. The brute-force rows
are computed in worker processes that import the code when each suite
starts, so the brute-force rows for the synthetic tiers very likely already
include the E3 change (their numbers equal E4's). The network rows and the
seed rows do not. No conclusion depends on this.

Reading: this helped. The same weights now solve more seed problems than
both references in both modes (28 vs 22 and 18 without backtracking; 32 vs 28
and 28 with search), where in M5 they did not. The untrained network did not
benefit from the spread (24 -> 22 without backtracking), so the gain is the
trained policy's knowledge becoming usable, not just extra randomness. Given
the noise caveat above, the comparisons with brute force are ties rather than
wins: 37 vs 35 seeds at 2,000 calls, 27.0% vs 23.0% on tier 4 at 128 calls,
38.5% vs 40.5% on tier 3 (128 network calls against 2,000 brute-force calls).
The clear differences are against the untrained references on every tier, and
against brute force on tier 2 (81.5% vs 66.0% at 128 calls).

Failure groups, network search with 128 calls (14 unsolved): too deep 2
(s33, s34); network did not find it 12 (s18, s24, s25, s31, s37, s38, s39,
s40, s41, s42, s43, s46). With 2,000 calls (9 unsolved): too deep 2; did not
find 7 (s37, s38, s39, s40, s42, s43, s46).

### E3. Commit when a case closes (search change, both solvers; commit `dd619f7`)

Change: when a move closes a case, both the network's best-first search and
the brute force drop every other state on the frontier and continue from
there. Among states that came from the same split this loses nothing (cases
share no facts, so the remaining cases are identical). Against states that
never made the split it is a heuristic: still safe, because each remaining
case knows everything the unsplit state knew, but possibly more expensive.
It targets the "too deep" group (s33, s34: two nested splits).

Brute force on seeds, before (E1) -> after: 128 calls 28 -> 28; 2,000 calls
35 -> 35; 20,000 calls 39 -> 41 (s33 and s34 solved;
`results/baseline_seed_*_commit.json`). Remaining at 20,000: s36, s37, s38,
s42, s46. The effect on the network is measured in E4's evaluation.

### E4. Retraining with the fixes (run `v2`), compared with `v1` at the same commit

Change: a new run from random weights with the same schedule and self-play
budget as `v1`, plus a *bundle* of training changes: proposals sampled at a
spread of temperatures during self-play, mirror augmentation (each proof also
learned with x and y exchanged), minimised proofs as training examples, and
length-sorted batches (which made iterations faster: 90 in 28 minutes instead
of 76). v2 was also *trained* in the environment that already had the E1
lemmas, the unique-root deduction and the E3 case commit, which v1's training
did not have. Because all of these changed together, a difference between
v1 and v2 cannot be attributed to any single one of them. One training seed each.

Both checkpoints were evaluated at commit `ae1b3a3` (so both use the lemmas
and the case commit), with **three sampling seeds** for the trained-network
rows; a range `a-b` is the minimum and maximum over the three. From here on
the seed benchmark has 50 problems (four three-variable problems added).
Commands: `alphafe eval --checkpoint checkpoints/v2/e4.pt --tag e4_v2 --seeds 3 --big-budget 2000`
and the same for v1. Tables below are produced by `scripts/compare_runs.py e4_v1 e4_v2`.

Number solved, held-out synthetic problems (200 per tier):

| solver | tier 1 | tier 2 | tier 3 | tier 4 |
|---|---|---|---|---|
| v1 network, no backtracking (32 calls) | 176-178 | 153-156 | 68-70 | 43-44 |
| **v2 network, no backtracking (32 calls)** | 179-180 | 155-159 | 79-81 | 46-51 |
| v1 network, search (128 calls) | 182-183 | 160-164 | 76-80 | 53-55 |
| **v2 network, search (128 calls)** | 185 | 168-172 | 84-89 | 56-58 |
| untrained network, no backtracking (32) | 148 | 102 | 42 | 27 |
| untrained network, search (128) | 169 | 129 | 65 | 41 |
| uniform policy, search (128) | 162 | 128 | 57 | 37 |
| brute force (128 calls) | 173 | 132 | 60 | 46 |
| brute force (2,000 calls) | 177 | 144 | 81 | 52 |
| brute force (20,000 calls) | 188 | 178 | 97 | 63 |

Number solved, seed benchmark (50 problems):

| solver | v1 | v2 |
|---|---|---|
| network, no backtracking (32 calls) | 30-32 | 32-35 |
| network, search (128 calls) | 34 | 35-38 |
| network, search (2,000 calls) | 41-42 | 43-44 |
| untrained network, no backtracking (32) / search (128) | 25 / 32 | |
| uniform policy, no backtracking (32) / search (128) | 14 / 29 | |
| brute force, 128 / 2,000 / 20,000 calls | 32 / 39 / 45 | |

v2 on the seed benchmark by difficulty (first sampling seed): no backtracking
21/22, 9/15, 1/11, 1/1, 0/1 for 0M, 5M, 10M, 15M, 20M; search with 128 calls
21/22, 14/15, 2/11, 1/1, 0/1; search with 2,000 calls 22/22, 15/15, 5/11, 1/1,
0/1. Brute force with 2,000 calls: 22/22, 12/15, 4/11, 1/1, 0/1.

Checker calls on the problems both solvers solve (v2, first sampling seed):

| suite | v2 search (128) vs brute force (128) | problems in common |
|---|---|---|
| seed | 3.5 vs 9.1 | 31 |
| tier 1 | 1.9 vs 4.3 | 172 |
| tier 2 | 2.9 vs 4.0 | 132 |
| tier 3 | 3.1 vs 6.6 | 59 |
| tier 4 | 4.3 vs 13.6 | 44 |

On the seed set, v2 search with 2,000 calls uses 70.1 calls against 107.9 for
brute force with 2,000 on the 38 problems both solve.

Time per problem in seconds (v2, first sampling seed):

| solver | seed | tier 1 | tier 2 | tier 3 | tier 4 |
|---|---|---|---|---|---|
| network, no backtracking (32 calls) | 0.044 | 0.018 | 0.046 | 0.088 | 0.153 |
| network, search (128 calls) | 0.085 | 0.027 | 0.081 | 0.172 | 0.370 |
| network, search (2,000 calls) | 0.915 | | | | |
| brute force (128 calls) | 0.015 | 0.006 | 0.017 | 0.040 | 0.051 |
| brute force (2,000 calls) | 0.155 | 0.065 | 0.218 | 0.580 | 0.800 |

So v2 with 128 calls takes about half the time brute force takes with 2,000
calls for comparable or better solve counts, but several times longer than
brute force with the same 128 calls.

**Reading.**

* *v2 against v1.* v2 is at least as good on every row, and the ranges do not
  overlap on tier 3 (both modes), on tier 2 and tier 1 with search, and on the
  seed set with 2,000 calls. Elsewhere they touch or overlap. With one
  training seed per run this says "the bundle probably helped, most clearly
  on nested-f problems", not more.
* *v2 against brute force at the same budget (128 calls).* Ahead on all four
  tiers; the margin is large on tiers 2 and 3 (about 37 and 26 problems of
  200) and small on tiers 1 and 4 (about 12 and 11).
* *v2 with 128 calls against brute force with 2,000.* Ahead on tier 2
  (168-172 vs 144), slightly ahead elsewhere (185 vs 177, 84-89 vs 81, 56-58
  vs 52); the last three are too close to call.
* *The ceiling.* Brute force with 20,000 calls still solves more than the
  network with 128 on every tier (188, 178, 97, 63). A fair summary: the
  network gets most of what brute force gets, for one to two orders of
  magnitude fewer checker calls, and has not yet shown it can reach problems
  that a big enough brute-force budget cannot, on the synthetic set.
* *Seed set (development set, see caveat).* v2 with 2,000 calls solves 43-44
  of 50 against 39 for brute force with 2,000 and 45 with 20,000. The sets
  differ: the network proves s36, s37 and s38, which brute force does not
  find even with 20,000 calls, while brute force with 20,000 gets s33, s34,
  s39, s40 and s43, which the network misses. Neither solves s42 or s46.
* The network was never trained on a three-variable problem, yet v2 solves
  all four three-variable seeds in every mode. (Four easy problems; do not
  read much into it.)

Failure groups for v2, search with 2,000 calls (first sampling seed, 7
unsolved): too deep (5+ creative moves): s33, s34. Network did not find it:
s39, s40, s42, s43, s46. `scripts/diagnose.py` on these shows the same
pattern each time: every move of the known proof can be written by the
network, but one "idea" step gets a probability around e^-10 to e^-20, for
example `y:=f(y)` in s42, `x:=x+y, y:=0` in s39, `y:=-f(x)` in s46. For
comparison, v1 gave the median hardest step of a seed proof log-probability
-15.5 and v2 gives it -10.8.

### E5. Exploration from expressions in the state (run `v3`): did not help

Hypothesis (from the E4 diagnosis): the network never learns "idea"
substitutions such as `y:=f(y)` because self-play almost never stumbles on
them, so let exploration propose terms that already occur in the state.
Change: in self-play, 2 of the 8 proposals per state substitute t, -t, v+t or
v-t for a variable v, where t is an f(...) or an argument of f taken from the
current identities; 1 proposal stays uniform-random (v2 had 2 uniform, 0 of
these). Everything else as v2. New run from random weights, 28 minutes, 96
iterations; evaluated at the same commit as E4 with three sampling seeds
(`results/e5_v3_*`). The heuristic is not used at evaluation time and is
unrelated to the brute-force baseline's term pool.

Number solved (ranges over three sampling seeds):

| solver | seed (50) | tier 1 | tier 2 | tier 3 | tier 4 |
|---|---|---|---|---|---|
| v2 network, no backtracking (32 calls) | 32-35 | 179-180 | 155-159 | 79-81 | 46-51 |
| v3 network, no backtracking (32 calls) | 32-33 | 180-182 | 156-163 | 77-80 | 49-50 |
| v2 network, search (128 calls) | 35-38 | 185 | 168-172 | 84-89 | 56-58 |
| v3 network, search (128 calls) | 34-37 | 184 | 161-163 | 81-84 | 53-56 |
| v2 network, search (2,000 calls) | 43-44 | | | | |
| v3 network, search (2,000 calls) | 43-45 | | | | |

Reading: no gain. v3 is level with v2 on the seed set and without
backtracking, and behind v2 with search on tier 2 (161-163 vs 168-172; the
ranges do not overlap) and probably tier 3. On the hand-proof diagnosis v3
does give the idea moves more probability (median hardest step -9.8 against
-10.8 for v2; `x:=f(y)` in s42 went from about 0.0001% to 0.7%), but not
enough to change what gets solved within the budgets, and the exploration
slots it took from the network's own proposals seem to have cost a little on
ordinary problems. With one training seed per run even the tier-2 gap could
be run-to-run variation. Kept in the code as an option (`n_subterm`), off by
default.

### E6. Twice the training (v2 resumed for another 28 minutes): little change

Change: `alphafe train --run v2 --resume --minutes 28`, nothing else. The run
went from 90 to 164 iterations (56 minutes in total, about 40,000 solve
examples in the buffer), staying on tier 4 with half of each batch of
problems drawn from the lower tiers. Evaluated with three sampling seeds at
commit `309879a`, which differs from E4's commit only in the ordering of an
exploration list that evaluation does not use (`results/e6_v2b_*`).

Number solved (ranges over three sampling seeds):

| solver | seed (50) | tier 1 | tier 2 | tier 3 | tier 4 |
|---|---|---|---|---|---|
| v2 at 28 min, no backtracking (32 calls) | 32-35 | 179-180 | 155-159 | 79-81 | 46-51 |
| v2 at 56 min, no backtracking (32 calls) | 33-34 | 178-179 | 160-167 | 78-79 | 49-52 |
| v2 at 28 min, search (128 calls) | 35-38 | 185 | 168-172 | 84-89 | 56-58 |
| v2 at 56 min, search (128 calls) | 36-40 | 186 | 170-176 | 88-91 | 53-57 |
| v2 at 28 min, search (2,000 calls) | 43-44 | | | | |
| v2 at 56 min, search (2,000 calls) | 41-45 | | | | |

Reading: a small gain on tier 2 (clear only without backtracking), everything
else inside the spread over sampling seeds. The held-out curve logged during
training is flat from about minute 20 onward
(`results/train_v2_log.json`). More of the same self-play is not what is
holding the network back; with this generator, budget and model size it has
roughly converged.

### E7. Ranking search states with the value head: did not help

Change: in best-first search, a state's priority becomes the log-probability
of its path plus log(value head's estimate), instead of the path
log-probability alone (`alphafe eval --value-weight 1.0`). No retraining;
weights are v2 at 56 minutes (E6). Three sampling seeds (`results/e7_value_*`).
The first attempt at this evaluation crashed on tier 3 with an out-of-memory
error on the Apple GPU (the value batches had free-form shapes); that was
fixed in commit `39d468d` and the evaluation rerun in full.

Number solved with search (ranges over three sampling seeds):

| ranking | seed, 128 calls | seed, 2,000 calls | tier 1 | tier 2 | tier 3 | tier 4 |
|---|---|---|---|---|---|---|
| path probability only (E6) | 36-40 | 41-45 | 186 | 170-176 | 88-91 | 53-57 |
| path probability + value | 35-40 | 42-43 | 185-187 | 167-169 | 86-89 | 57 |

Reading: no gain, and slightly worse on tier 2. The value head is trained on
noisy labels (a state counts as "unsolvable" whenever a 48-call attempt
failed), so this is not surprising. The option stays in the code, off by
default.

## Where things stand after M6

**Soundness.** In every evaluation run to date, each proof found for a
problem with a recorded answer produced exactly the recorded answer (the
`AnswerMismatch` canary never fired). The model-check fuzzer has tested about
100,000 accepted random moves on the 50 seed problems and 110,000 on 1,600
synthetic problems against known solutions without a violation. The one
discrepancy it ever reported was in the answer canonicaliser, not in a proof
move (`x^2 - a^2 + b` was not recognised as `x^2 + c`); fixed before M3.

**What works.**

* 0M and 5M seed problems: the network with search solves all 37 given 2,000
  checker calls, and 35-36 of them within 128 (first sampling seed of E4 and E6).
* On problems both solve, the trained network needs fewer checker calls than
  brute force: about a quarter to a half as many without backtracking, and
  between half and nine tenths as many with search (E6). At equal small
  budgets it also solves more held-out problems, clearly so on tiers 2 and 3.
* Three seed problems (s36, s37, s38) have network proofs and no brute-force
  proof at 20,000 calls with the default search.

**What does not.**

* 10M: 4-5 of 11 with 2,000 calls. s33 and s34 (two nested case splits, 7
  creative moves) have never been solved by the network; s40, s42 and the 20M
  problem s46 neither. Over all runs so far the trained network has solved 45
  of the 50 seed problems at least once, brute force 48 (using budgets up to
  50,000 calls), and s46 has been solved by nothing.
* A large enough brute-force budget still beats the network at 128 calls on
  every held-out tier (188/178/97/63 of 200 at 20,000 calls).
* More training time (E6), state-derived exploration (E5) and value-guided
  search (E7) each made no measurable difference.

**Experiments that helped:** lemmas over Q (E1), sampling proposals at a
spread of temperatures (E2), committing when a case closes (E3, for brute
force at large budgets), and the retraining bundle of E4.
**Experiments that did not:** E5, E6, E7.

**What we would try next**, in order: (1) a generator that produces problems
whose proofs need the "idea" substitutions the network lacks, including
three-variable problems; (2) several training seeds, to find out which of the
small differences above are real; (3) a larger self-play budget on tiers 3-4
together with a cleaner value target; (4) product reasoning and wider
injectivity/surjectivity criteria in the checker.

## M7: the real benchmark, version 1 baseline

### Protocol (written and committed before the run)

The real benchmark (`benchmarks/real/real.jsonl`, 137 competition problems)
was compiled without running the solver. This is the solver's first contact
with it, and the point of the run is to record what version 1 does on unseen
problems before anything is changed in response.

* **Solver.** The code as it was when the benchmark was compiled (commit
  `a199cda`), plus changes to the evaluation harness only: suite selection,
  provenance, mismatch handling, flagged-problem tables, and an equation the
  checker cannot load being scored as unsolved. No move, search rule, pool
  or weight was changed. The harness check below shows the numbers of an
  existing run are reproduced.
* **Weights.** The published file `alphafe-v2-56min.pt` (release `v0.1.0`,
  sha256 `8f52cc59...9bee3`), the same weights as E6.
* **Command.** `alphafe eval --suite real --tag v1 --checkpoint
  checkpoints/alphafe-v2-56min.pt --seeds 3 --big-budget 2000`, run once from
  a clean tree on the Apple GPU, followed by `python
  scripts/run_baseline.py 20000 120 widening v1 --suite real` for brute force at
  20,000 calls.
* **Rows.** The trained network without backtracking (32 calls), with search
  at 128 and at 2,000 calls, each with three sampling seeds; the untrained
  network and the uniform policy at 32 and 128; brute force at 128, 2,000 and
  20,000.
* **Tables.** Each on all 137 problems and again on the 124 that carry no
  flag (12 are flagged as seen in development and 1 as in the training
  pool), and by MOHS value. The flagged-free numbers are obtained by
  filtering the rows of the one run, since a second run on a smaller suite
  would draw different samples.
* **What counts.** The headline is the 124-problem table. The 12 problems
  seen in development are mostly ones the solver was already known to fail
  on, so including them lowers the rate; they are reported and not hidden.
  132 of the 137 MOHS values are estimates, so the MOHS columns are a rough
  grouping.
* **Harness check.** Before the run, the changed harness was run on the
  seed suite with the same weights, seeds and budgets as E6 (`e6_v2b`). All
  nine result files came out identical to the committed ones, row for row,
  in which problems are solved and in checker calls (network rows for all
  three sampling seeds: 34/34/33, 40/37/36 and 42/41/45). `git diff --stat
  a199cda -- alphafe/` at the run commit touches `eval.py` (the harness),
  `benchcheck.py` and `baseline/guesser.py` (validator, exponent limit),
  and a few lines each in `checker.py`, `env.py`, `search.py`,
  `baseline/search.py`, `bench.py`, `cli.py`, `terms.py` and `train.py`, all
  for reporting an unloadable equation or a mismatch.
* **If something goes wrong.** An answer mismatch stops everything else: the
  record is re-read against its source, and if the record is right it is a
  soundness bug that outranks all other work. If a harness bug forces a
  second run, both runs are reported.

### Result

Run at commit `a82d869`, clean tree, Apple GPU, 42 minutes for the network
and reference rows and 3 minutes for brute force at 20,000 calls. Files:
`results/v1_real_*.json`, `results/v1.md`, `results/baseline_real_20000_v1.json`.
No checked proof gave an answer different from the recorded one.

Solved, of the 124 problems that carry no flag (the headline) and of all 137:

| solver | 124 unflagged | all 137 | per sampling seed (137) |
|---|---|---|---|
| network, no backtracking (32 calls) | 6 (4.8%) | 10 (7.3%) | 10, 12, 11 |
| network, search (128 calls) | 10 (8.1%) | 14 (10.2%) | 14, 13, 13 |
| network, search (2,000 calls) | 13 (10.5%) | 17 (12.4%) | 17, 17, 17 |
| untrained network, no backtracking (32) | 5 (4.0%) | 8 (5.8%) | |
| untrained network, search (128) | 5 (4.0%) | 8 (5.8%) | |
| uniform policy, no backtracking (32) | 4 (3.2%) | 7 (5.1%) | |
| uniform policy, search (128) | 6 (4.8%) | 9 (6.6%) | |
| brute force (128 calls) | 5 (4.0%) | 8 (5.8%) | |
| brute force (2,000 calls) | 8 (6.5%) | 12 (8.8%) | |
| brute force (20,000 calls) | 12 (9.7%) | 16 (11.7%) | |

The network rows show the first sampling seed. The three seeds do not solve
quite the same problems: at 2,000 calls 19 of the 137 are solved by at least
one seed.

By MOHS value, on the 124 unflagged problems (132 of the 137 values are
estimates):

| solver | 0M | 5M | 10M | 15M | 20M | 25M and up |
|---|---|---|---|---|---|---|
| network, search (128 calls) | 2/2 | 7/15 | 1/43 | 0/32 | 0/19 | 0/13 |
| network, search (2,000 calls) | 2/2 | 7/15 | 4/43 | 0/32 | 0/19 | 0/13 |
| brute force (2,000 calls) | 2/2 | 5/15 | 1/43 | 0/32 | 0/19 | 0/13 |
| brute force (20,000 calls) | 2/2 | 6/15 | 4/43 | 0/32 | 0/19 | 0/13 |

### Plain reading

* **Version 1 solves about one real problem in ten.** The seed benchmark,
  which was written for the project and used to choose fixes, gave 41 to 45
  of 50 for the same weights and budget. The real benchmark gives 13 of 124.
  The seed numbers were never an estimate of this, and RESULTS says so
  above, but the size of the gap is the main finding of this run.
* **Nothing rated 15M or above is solved by any solver**, and only 4 of 43
  problems at 10M. The stated target of version 1 was 0M to 10M: on the 60
  unflagged problems in that range the best row (network search, 2,000 calls)
  solves 13, or 22%. Counting any solver at any budget in this run, 18 of
  the 124 are solved (22 of 137).
* **The ordering of the solvers is the same as on the other benchmarks.** At
  equal checker calls the trained network solves more than brute force (10
  against 5 at 128 calls, 13 against 8 at 2,000) and the untrained network
  and the uniform policy solve the fewest. With 137 problems and counts this
  small the differences are a handful of problems each; no significance
  test was run, and none of these gaps should be read as established.
* **More budget helps little.** From 128 to 2,000 calls the network gains 3
  problems. Brute force at ten times the network's largest budget (20,000
  calls) reaches 12, one fewer than the network at 2,000. Each solves
  problems the other does not: taking every sampling seed, the network at
  2,000 calls has 6 that brute force at 20,000 lacks, and brute force has 3
  the other way round. Every unsolved row stopped on its budget; no
  brute-force row reached the 120 second limit (the slowest took 37 s).
* **The flagged problems are easier for the solver than the rest**, not
  harder as the protocol expected: 4 of the 13 are solved (the one in the
  training pool, the one that is a seed problem after a change of variables,
  and two of the 11 from the design study, both of which that study had
  already found to be solvable). Leaving them out lowers the rate from 12.4%
  to 10.5%.
* **Two problems cannot be loaded** (exponents 2021 and 2015) and count as
  unsolved in every row.
* **What the run does not show.** Why each problem fails. The design study
  behind issue #99 found, on a different and hand-picked set, that most
  failures were missing routine deductions and search depth and a minority
  were gaps in the move language. That is the working hypothesis for the
  next milestone. It was not checked on this benchmark, and the unsolved
  real problems have not been inspected, so that nothing is tuned on them.
