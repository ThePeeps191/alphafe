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
P(y, y) gives f(y)^2 = f(0).
P(-y, y) gives f(0)f(y)^2 = f(-2y).
Putting x = 0 in f(x)^2 = f(0) gives f(0)^2 = f(0).
Since f(0)^2 = f(0), we have f(0) = 0 or f(0) = 1.

Case f(0) = 0.
Hence f(x) = 0 for all x.
Substituting this into the original equation and comparing coefficients, it holds exactly for: f(x) = 0.

Case f(0) = 1.
Hence f(x) = 1 for all x.
Substituting this into the original equation and comparing coefficients, it holds exactly for: f(x) = 1.

All cases are closed. Every function listed in the answer was substituted into the original equation and satisfies it exactly, and the argument above shows there are no others.
```

The design follows [AlphaGeometry](https://www.nature.com/articles/s41586-023-06747-5)
(Trinh et al., *Nature* 2024). A symbolic engine defines the legal proof moves
and makes the routine deductions. A small neural network, trained from random
weights on its own attempts, proposes the moves that need an idea:
substitutions, case splits and preimages. AlphaFE is not affiliated with
Google DeepMind.

When AlphaFE cannot find a proof it says so. All it prints then is a guess
among polynomials of degree at most 2, labelled as a guess. That is the usual
outcome on competition problems today: on a benchmark of 137 real ones,
version 1 finds a proof for about one in ten (see [Results](#results)).

## Quick start

You need Python 3.11 or newer (tested on 3.12) and [uv](https://docs.astral.sh/uv/).
Everything installs into a project virtual environment.

```sh
git clone https://github.com/ThePeeps191/alphafe.git
cd alphafe
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python -e ".[dev]"
.venv/bin/python -m pytest            # about 400 tests, around ten seconds
```

Download the trained network (10 MB) from the
[v0.1.0 release](https://github.com/ThePeeps191/alphafe/releases/tag/v0.1.0):

```sh
mkdir -p checkpoints
curl -L -o checkpoints/best.pt \
  https://github.com/ThePeeps191/alphafe/releases/download/v0.1.0/alphafe-v2-56min.pt
shasum -a 256 checkpoints/best.pt
# 8f52cc591dd8a470d2b84966d471050b639d689765b895026e2f8f15b639bee3
```

Then solve something:

```sh
.venv/bin/alphafe solve "f(x+y) = f(x) + y" --domain R
.venv/bin/alphafe solve "f(x-y) = f(x)f(y)" --domain R
```

Without `checkpoints/best.pt`, `solve` uses brute-force search and says so.
Proposals are sampled, so the proof and the number of checker calls vary from
run to run. The weights match the tokenizer and model at the `v0.1.0` tag;
after a change to either, retrain.

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
# or on one of them (--suite seed, real or synthetic).
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

On real problems the solver is weak. The real benchmark is 137 competition
problems that fit the scope above, selected by rules fixed in advance and not
looked at during development. Version 1 was run on it once, before anything
was changed in response.

| | network, search (128 calls) | network, search (2,000 calls) | brute force (2,000 calls) | brute force (20,000 calls) |
|---|---|---|---|---|
| 124 problems never seen in development | 10 | 13 | 8 | 12 |
| all 137 | 14 | 17 | 12 | 16 |

That is about one problem in ten. The solved ones are rated 0M to 10M, and
nothing rated 15M or above is solved by any solver. In the target range of
0M to 10M the best row solves 13 of 60. The counts are small, so the gaps
between solvers are a few problems each. `RESULTS.md` (M7) has the protocol,
which was committed before the run, and the full tables.

### Synthetic and seed problems

These are the problems the solver was developed on, and they are much easier
than the real ones.

Problems solved, out of 200 per held-out tier and 50 on the seed benchmark.
The network was trained once, for 28 minutes on a laptop GPU, and evaluated
with three sampling seeds; a range is the minimum and maximum over those
seeds. A "call" is one move sent to the checker.

| | network, no backtracking (32 calls) | network, search (128 calls) | brute force (128 calls) | brute force (2,000 calls) |
|---|---|---|---|---|
| held-out synthetic, tier 1 | 179-180 | 185 | 173 | 177 |
| held-out synthetic, tier 2 | 155-159 | 168-172 | 132 | 144 |
| held-out synthetic, tier 3 | 79-81 | 84-89 | 60 | 81 |
| held-out synthetic, tier 4 | 46-51 | 56-58 | 46 | 52 |
| seed benchmark | 32-35 | 35-38 | 32 | 39 |

At an equal small budget the trained network solves more than brute force,
most clearly on tiers 2 and 3. On problems both solve, the network without
backtracking needs a quarter to a half as many checker calls. Brute force
with 20,000 calls still solves more held-out problems than the network does
with 128 (188, 178, 97 and 63 on the four tiers). A network proposal also
costs far more time than a checker call, so the network saves checker calls
and does not save seconds.

On the seed benchmark with 2,000 calls the network solves 43-44 of 50, against
39 for brute force at 2,000 calls and 45 at 20,000. That covers all 37 problems
rated 0M or 5M and 5 of the 11 rated 10M (first sampling seed). The single 20M
problem has not been solved by anything. Three seed problems had a network
proof and no brute-force proof at 20,000 calls, and five went the other way.

No proof accepted by the checker has produced an answer different from a
recorded one.

The network in the quick start is the same training run after 56 minutes. It
scores about the same (experiment E6 in `RESULTS.md`), and the 28-minute
weights are in the release as `alphafe-v2-28min.pt`.

The seed benchmark was used to choose fixes during development, so its
numbers are optimistic. Each configuration was trained with a single seed, so
small differences between runs may be noise. `RESULTS.md` has every
measurement, including the first trained network, which did worse than an
untrained one on the seed benchmark, and three experiments that made no
difference.

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
proved nonzero, and "additive implies linear" only over Q. Every claimed
solution is substituted back into the original equation.

The network is a 2.5M-parameter encoder-decoder transformer. It reads the
current proof state and writes the next move token by token under a grammar
that permits only well-formed moves. Search either follows its best accepted
proposal without backtracking or keeps a frontier and expands the most likely
state first.

Training is self-play on synthetic problems. Proofs the checker accepts
become training examples, and so do the identities derived in failed
attempts, each as an example of how to reach that identity. No external model
or API is called anywhere, and the brute-force baseline is never used to
produce training data.

`docs/DESIGN.md` has the move reference, the full list of soundness rules and
a map of the modules.

## Benchmarks

* `benchmarks/seed/`: 50 classic easy problems written for this project, four
  of them in three variables, with verified answers, estimated MOHS ratings
  and 48 checked proofs. Two pairs are the same equation with x and y
  exchanged, so 48 are distinct. Treat it as a development set.
* `benchmarks/synthetic/heldout.jsonl`: 800 generated problems, 200 per
  curriculum tier, frozen in a file and excluded from training by a hash of
  the canonical equation.
* `benchmarks/real/`: 137 real competition problems, used only for testing.
  They were selected by rules fixed in advance from MathNet and Evan Chen's
  solution notes, and `benchmarks/real/SKIPPED.md` lists everything the rules
  covered and left out. Thirteen are flagged as not fully unseen, and results
  are given with and without them.

## Known limits

* The checker recognises injectivity and surjectivity by syntactic patterns,
  which cover fewer arguments than a person can make.
* No move multiplies an identity by an expression.
* The generator produces two-variable problems only, so the network has never
  trained on a three-variable problem, though the four in the seed benchmark
  are solved.
* Most seed problems the network misses hinge on one substitution to which it
  gives almost no probability (`scripts/diagnose.py` shows which). Two others
  need two nested case splits.

## More

* `RESULTS.md`: every measurement, including the ones that did not help.
* `DECISIONS.md`: design choices, one line each.
* `PROGRESS.md`: what is done and what to try next.
* `docs/DESIGN.md`: moves, soundness rules, modules.
* `docs/EXTENDING.md`: adding a move, running an experiment.

MIT licence.
