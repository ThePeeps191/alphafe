# AlphaFE

AlphaFE solves easy olympiad functional equations. Give it an equation and it
finds every function that satisfies it, with a proof that an exact symbolic
checker has accepted step by step.

```
$ alphafe solve "f(x-y) = f(x)f(y)" --domain R

Problem. Find all functions f: R -> R such that f(x-y) = f(x)f(y) for all real x, y.

Answer. f(x) = 0; f(x) = 1.

Solution. Let P(x, y) denote the assertion f(x-y) = f(x)f(y).
P(0, y) gives f(-y) = f(0)f(y).
P(x, 0) gives f(0)f(x) = f(x).
So f is even: f(-t) = f(t) for all t.
P(x, x) gives f(x)^2 = f(0).
P(x, -x) gives f(-x)f(x) = f(2x).
With the relations already known, this becomes f(x)^2 = f(2x).
Together with the earlier relations this yields f(2x) = f(0).
Hence f(x) = f(0) for all x.
Substituting this into the original equation and comparing coefficients, it holds exactly for: f(x) = 0; f(x) = 1.

All cases are closed. Every function listed in the answer was substituted into the original equation and satisfies it exactly, and the argument above shows there are no others.
```

The design follows [AlphaGeometry](https://www.nature.com/articles/s41586-023-06747-5)
(Trinh et al., *Nature* 2024). A symbolic engine defines the legal proof moves
and makes the routine deductions, including the standard opening
substitutions (the example above needs nothing else). A search then proposes
the moves that need an idea: other substitutions, case splits and preimages.
It runs as plain brute force, or as a sampling search over proposals from a
small neural network trained from random weights on its own attempts. So far
the training adds little: on real problems the same search with random
weights does about as well (see [Results](#results)). AlphaFE is not
affiliated with Google DeepMind.

When AlphaFE cannot find a proof it says so. All it prints then is a guess
among polynomials of degree at most 2, labelled as a guess. On competition
problems that is still the more common outcome: on a benchmark of 137 real
ones it finds a proof for about a third (see [Results](#results)).

## Quick start

You need Python 3.11 or newer (tested on 3.12) and [uv](https://docs.astral.sh/uv/).
Everything installs into a project virtual environment.

```sh
git clone https://github.com/ThePeeps191/alphafe.git
cd alphafe
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python -e ".[dev]"
.venv/bin/python -m pytest            # about 680 tests
```

Download the trained network (10 MB) from the
[v0.3.0 release](https://github.com/ThePeeps191/alphafe/releases/tag/v0.3.0):

```sh
mkdir -p checkpoints
curl -L -o checkpoints/best.pt \
  https://github.com/ThePeeps191/alphafe/releases/download/v0.3.0/alphafe-m3-150min.pt
shasum -a 256 checkpoints/best.pt
# e52bcd02665f22f3ff2f44253e50aa8a83170aa1390a56b361805aa6f4ca63af
```

Then solve something:

```sh
.venv/bin/alphafe solve "f(x+y) = f(x) + y" --domain R
.venv/bin/alphafe solve "f(x-y) = f(x)f(y)" --domain R
```

Without `checkpoints/best.pt`, `solve` uses brute-force search and says so.
Proposals are sampled, so the proof and the number of checker calls vary from
run to run unless you pass `--seed`. A checkpoint records the token vocabulary
it was trained with, and loading one that does not match the code is
refused. The v0.2.0 weights still load and were not measurably worse on the
development sets.

## Commands

```sh
# Find all solutions and print the proof.
.venv/bin/alphafe solve "f(x)f(y) = f(x+y) + xy" --domain R

# Check a proof you wrote yourself (format in docs/DESIGN.md).
.venv/bin/alphafe check "f(x+y) = f(x) + y" --domain R --proof my.proof

# Train by self-play. Each invocation runs for the given time and can be resumed.
.venv/bin/alphafe train --run myrun --minutes 28
.venv/bin/alphafe train --run myrun --minutes 28 --resume
cp checkpoints/myrun/last.pt checkpoints/best.pt

# Compare the network, an untrained network and brute force on all benchmarks,
# or on one of them (--suite seed, dev, real or synthetic).
.venv/bin/alphafe eval --checkpoint checkpoints/best.pt
.venv/bin/alphafe eval --checkpoint checkpoints/best.pt --suite real
```

Equations use `+ - *`, powers such as `x^2`, juxtaposition for products
(`2x`, `xf(y)`) and division by integer literals only (`x/2`). The domain is
`R` or `Q`. Variables may be any of `x y z t u v w`; `solve` renames other
letters to `x`, `y`, `z` and says so. A malformed equation or proof file
gives a one-line error and exit status 2. Status 1 means no proof was found
(`solve`) or the proof was not accepted (`check`).

## What it can solve

Version 1 handles one unknown function f from R to R or from Q to Q, in an
equation that holds for all values of up to three variables and is built from
variables, rational constants, `+`, `-`, `*` and f. The task is always to find
all such f, and the answer must be a set of polynomial families with rational
coefficients, such as `f(x) = cx + d`.

A problem whose answer needs `sqrt(2)`, or that has non-polynomial solutions
(Cauchy's equation over R), comes back as unsolved. Positive-real or integer
domains, inequalities, division by variables, several unknown functions, and
hypotheses such as continuity or monotonicity are not supported.

Difficulty is measured on Evan Chen's MOHS scale, which runs from 0M to 50M;
30M is a medium-hard IMO problem. The target range is 0M to 10M.

## Results

### Real competition problems

The real benchmark is 137 competition problems that fit the scope above,
selected by rules fixed in advance. For the three runs below, thirteen were
flagged as seen during development and the other 124 had never been looked
at; those 124 are the headline. Each version is run on the benchmark once,
under a protocol committed before the run. Four more problems were flagged
after the third run, to find out why they were no longer solved, so later
runs have 120 unseen problems.

Solved, of the 124:

| | network, search (128 calls) | network, search (2,000 calls) | untrained network, search (2,000 calls) | brute force (2,000 calls) | brute force (20,000 calls) |
|---|---|---|---|---|---|
| v0.1.0 | 10 | 13 | not run | 8 | 12 |
| v0.2.0 | 28 | 43 | not run | 27 | 38 |
| v0.3.0 | 35 | 45 | 44 | 38 | 43 |

About a third of real problems in scope are solved (45 of 124, 36%). In the
target range of 0M to 10M the best row solves 33 of 60. Above it, 6 of 32
problems rated 15M are solved, 5 of 19 rated 20M and 1 of 13 rated 25M or
more. On all 137 the best row solves 56.

From v0.1.0 to v0.2.0 the count tripled. The environment began to make the
routine substitutions by itself (the standard openings, the swap, instances
of identities already found), two lemmas about squares were added, and the
network was retrained.

From v0.2.0 to v0.3.0 the best row gained two problems, which is within the
spread of the sampling seeds (44 to 47 now, 42 to 43 before). What changed
is the cheap end: the set of opening substitutions grew and the search began
to take proposals from expressions already on the page, so the rows without
a trained network roughly doubled at small budgets. The routine moves alone,
with no search, now solve 24 of the 124, against 8 before. Four problems
that v0.2.0 solved are no longer solved by any row.

The trained network is not what solves these problems. With random weights
the same search solves 44 at 2,000 calls against 45, and 35 at 128 calls
against 35. The network row beats brute force at equal budget, but so does
the untrained network, so that lead belongs to the search and the way it
builds proposals and not to the weights.
Training was 150 minutes of self-play on one laptop; most generated problems
are solved before any search starts, so it saw few proofs longer than two
moves. Issue #107 has the diagnosis and what is being tried.

A "call" is one move sent to the checker. The network rows are the first of
three sampling seeds. Each version is one training run. `RESULTS.md` (M7, M8
and M9) has the protocols and the full tables.

### Synthetic and seed problems

These are the problems the solver was developed on. They are much easier
than the real ones, and choices between versions are made on them.

Problems solved, out of 200 per held-out tier, 51 on the seed benchmark and
32 on the development suite; a range is the minimum and maximum over three
sampling seeds.

| | network, no backtracking (32 calls) | network, search (128 calls) | untrained network, search (128 calls) | brute force (128 calls) | brute force (2,000 calls) |
|---|---|---|---|---|---|
| held-out synthetic, tier 1 | 188-189 | 189-190 | 186 | 188 | 190 |
| held-out synthetic, tier 2 | 193 | 193-194 | 188 | 191 | 194 |
| held-out synthetic, tier 3 | 139-140 | 139-141 | 140 | 138 | 144 |
| held-out synthetic, tier 4 | 103-105 | 107-109 | 104 | 97 | 114 |
| seed benchmark | 45-48 | 45-46 | 47 | 47 | 50 |
| development suite | 19-22 | 20-23 | 21 | 18 | 23 |

Training is worth three to six problems on tiers 1, 2 and 4 at 128 calls and
nothing on tier 3, the seed benchmark or the development suite. Brute force
with 2,000 calls matches or beats the network with 128 everywhere. With 2,000 calls the network solves all 51
seed problems and 23 or 24 of the development suite. The routine moves
alone, without any search, solve 182, 179, 120 and 78 of the four tiers.
Many held-out problems in tiers 3 and 4 have no proof at all, so 200 is not
the ceiling.

A network proposal costs far more time than a checker call, so the network
row is slower than brute force at the same number of calls: about 18 seconds
per real problem at 2,000 calls against under 3.

No proof accepted by the checker has produced an answer different from a
recorded one.

The seed benchmark and the development suite were used to choose fixes, so
their numbers are optimistic; IMO 1992/2, for one, is in the development
suite and is now solved by the routine moves and the square lemmas with no
search. `RESULTS.md` has every measurement, including the experiments that
made no difference.

## How it works

A proof is a list of moves applied to the original equation: substitute
values for variables, split into cases on a fact about constants, cancel f
after proving injectivity, and so on. The checker applies each move with
exact rational arithmetic and rejects any step it cannot justify. It also
makes the routine deductions (combining identities, rewriting, using proven
properties such as oddness) without being asked, so a move is needed only
where a person would need an idea.

The checker is the only trusted component. The standard mistakes are blocked
by rule: case splits are allowed only on facts without variables,
cancellation only after injectivity is proved, division only by constants
proved nonzero, and "additive implies linear" only over Q (over R it needs
f(x^2) = f(x)^2 as well). Every claimed
solution is substituted back into the original equation.

The network is a 2.5M-parameter encoder-decoder transformer. It reads the
current proof state and writes the next move token by token under a grammar
that permits only well-formed moves. Search either follows its best accepted
proposal without backtracking or keeps a frontier and expands the most likely
state first. A search with backtracking also tries, next to the network's
proposals, a few substitutions built from expressions that are already on
the page, because a trained policy gives some kinds of move (`x := f(x)`, for
one) almost no probability.

Training is self-play on synthetic problems. Proofs the checker accepts
become training examples, and so do the identities derived in failed
attempts, each as an example of how to reach that identity. No external model
or API is called anywhere, and the brute-force baseline is never used to
produce training data.

`docs/DESIGN.md` has the move reference, the full list of soundness rules and
a map of the modules.

## Benchmarks

* `benchmarks/seed/`: 51 problems with verified answers, estimated MOHS
  ratings and 49 checked proofs. Fifty are classic easy problems written for
  this project, four of them in three variables; two pairs are the same
  equation with x and y exchanged. The last is USAMO 2002/4, added with the
  lemma it needed. Treat it as a development set.
* `benchmarks/synthetic/heldout.jsonl`: 800 generated problems, 200 per
  curriculum tier, frozen in a file and excluded from training by a hash of
  the canonical equation.
* `benchmarks/synthetic/planted.jsonl`: 600 generated problems hidden behind
  one to three changes of variables, 200 each with a known proof of 2, 3 and
  4 proposed moves. Also excluded from training. Evaluated on request with
  `--suite planted`.
* `benchmarks/dev/`: a development suite of 36 harder problems, mostly rated
  10M and above, with 13 checked proofs. It may be tuned on, so it says what
  to work on next and not how good the solver is. Twenty are hand-picked and
  sixteen are the real problems flagged as seen in development (32 problems
  in the results above, before four were flagged).
* `benchmarks/real/`: 137 real competition problems, used only for testing.
  They were selected by rules fixed in advance from MathNet and Evan Chen's
  solution notes, and `benchmarks/real/SKIPPED.md` lists everything the rules
  covered and left out. Seventeen are flagged as not fully unseen, and results
  are given with and without them.

## Known limits

* The checker recognises injectivity and surjectivity by syntactic patterns,
  which cover fewer arguments than a person can make.
* No move multiplies an identity by an expression.
* The generator produces two-variable problems only, so the network has never
  trained on a three-variable problem, though the four in the seed benchmark
  are solved.
* Training does not yet improve on random weights for real problems. The
  network is shown only the first 14 identities of a proof state, and an
  unsolved starting state has a median of 25. Self-play problems are mostly
  solved by the routine moves, so few proofs with several proposed moves
  reach the trainer.
* On hand-written proofs of development problems the network gives the
  needed move almost no probability at some step (`scripts/diagnose.py`
  shows where), and three of eight such proofs contain a move its grammar
  cannot write.

## More

* `RESULTS.md`: every measurement, including the ones that did not help.
* `DECISIONS.md`: design choices, one line each.
* `PROGRESS.md`: what is done and what to try next.
* `docs/DESIGN.md`: moves, soundness rules, modules.
* `docs/EXTENDING.md`: adding a move, running an experiment.

MIT licence.
