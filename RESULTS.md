# Results

Every number here was produced by the code in this repository. Each run is
saved under `results/` (JSON, one row per problem, with the found proof).
Negative results stay in.

**Definitions.** "Solved" means a complete proof was found *and* re-checked
from scratch by `checker.check`; if a recorded answer exists, the proof's
solution set must equal it (a mismatch aborts the run instead of being
scored). "Checker calls" counts proposed moves sent to the checker, accepted
or not; the free moves applied automatically after each proposal (conclude,
cauchy, inj, surj, cancel) are not counted.

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

The real benchmark is empty (the owners have not added problems yet).

### Plain reading

1. **On problems like its training data, the network learned something real.**
   On every held-out tier it solves more than the untrained network and the
   uniform policy, and it needs about one checker call where they need 4-10.
   With 128 calls it beats brute force at the same budget on all four tiers,
   and on tiers 1-2 it beats brute force given 15 times more calls.
2. **It does not beat brute force everywhere.** With 2,000 calls brute force
   is ahead on tier 3 (40.0% vs 36.5%) and level on tier 4.
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
5. One thing the network did that the authors had not: it proved s36,
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
