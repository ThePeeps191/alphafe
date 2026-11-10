# AlphaFE

A solver for easy olympiad **functional equations**, for example

> Find all f: R -> R with f(x + y) = f(x) + y for all real x, y.

AlphaFE outputs the full solution set together with a proof that the listed
functions work and nothing else does, and every step of that proof has been
accepted by an exact symbolic checker.

The design follows [AlphaGeometry](https://www.nature.com/articles/s41586-023-06747-5)
(Trinh et al., *Nature* 2024): an exact symbolic engine defines the legal proof
moves and does the routine deductions, and a small neural network, trained
from scratch on its own attempts, proposes the creative moves. AlphaGeometry
is the inspiration for this project. AlphaFE is an independent hobby project
by two olympiad students and is not affiliated with DeepMind.

* `RESULTS.md`: every measurement, including the ones that did not help.
* `DECISIONS.md`: design choices, one line each.
* `PROGRESS.md`: what is done and what is next.

## Where it stands

Numbers from `RESULTS.md` (experiment E4; one training run of 28 minutes on a
laptop GPU, three sampling seeds, ranges shown):

| | network, no backtracking (32 checker calls) | network, search (128 calls) | brute force (128 calls) | brute force (2,000 calls) |
|---|---|---|---|---|
| held-out synthetic, tier 1 (200) | 179-180 | 185 | 173 | 177 |
| held-out synthetic, tier 2 (200) | 155-159 | 168-172 | 132 | 144 |
| held-out synthetic, tier 3 (200) | 79-81 | 84-89 | 60 | 81 |
| held-out synthetic, tier 4 (200) | 46-51 | 56-58 | 46 | 52 |
| seed benchmark (50) | 32-35 | 35-38 | 32 | 39 |

With 2,000 calls the network solves 43-44 of the 50 seed problems; brute force
solves 39 with 2,000 calls and 45 with 20,000.

What this does and does not show:

* The checker has accepted no wrong answer: every proof found for a problem
  with a recorded answer produced exactly that answer.
* The trained network is clearly better than the same network untrained and
  than random proposals, and it finds proofs with far fewer checker calls than
  brute force (about 2-4 against 4-14 on problems both solve).
* Against brute force with a much larger budget the picture is mixed: the
  network proves three seed problems brute force cannot (and one the authors
  thought was out of reach), and misses five that brute force gets.
* The first trained network was *worse* than an untrained one on the seed
  set; `RESULTS.md` explains why and what fixed it.
* 0M and 5M seed problems are essentially solved (37 of 37 with search and
  2,000 calls); 10M is at 5 of 11; the single 20M problem is unsolved.
* The seed set was used to choose fixes, so it is a development set. The real
  benchmark is empty until the owners fill it.

## Setup

Everything lives in a project virtual environment; nothing is installed globally.

```sh
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python -e ".[dev]"
.venv/bin/python -m pytest            # about a minute
```

Dependencies: Python 3.11+, PyTorch; pytest, hypothesis and SymPy for tests.
No external LLM or API is called anywhere.

## Using it

```sh
# Solve: prints a polynomial guess, the answer, the proof moves and a write-up.
.venv/bin/alphafe solve "f(x+y) = f(x) + y" --domain R
.venv/bin/alphafe solve "f(x + f(y)) = f(x) + y" --domain Q

# Check a proof you wrote yourself (format below).
.venv/bin/alphafe check "f(x+y) = f(x) + y" --domain R --proof my.proof

# Train the network by self-play (resumable; about 28 minutes per invocation).
.venv/bin/alphafe train --run myrun --minutes 28
.venv/bin/alphafe train --run myrun --minutes 28 --resume
cp checkpoints/myrun/last.pt checkpoints/best.pt

# Evaluate network vs untrained network vs brute force on all benchmarks.
.venv/bin/alphafe eval --checkpoint checkpoints/best.pt
```

`alphafe solve` uses the network if `checkpoints/best.pt` exists and falls back
to the brute-force baseline otherwise (checkpoints are not committed). It says
which one found the proof. Input syntax: `+ - *`, powers `x^2`, juxtaposition
(`2x`, `xf(y)`), division by integer literals only (`x/2`).

Example output:

```
Problem. Find all functions f: R -> R such that f(x)f(y) = f(x+y) + xy for all real x, y.

Answer. f(x) = 1 - x; f(x) = x + 1.

Solution. Let P(x, y) denote the assertion f(x)f(y) = f(x+y) + xy.
P(0, 0) gives f(0)^2 = f(0).
Since f(0)^2 = f(0), we have f(0) = 0 or f(0) = 1.

Case f(0) = 0.
P(x, 0) gives f(x) = 0.
Hence f(x) = 0 for all x.
Substituting this into the original equation, no choice of the constants works, so this case gives no solutions.

Case f(0) = 1.
P(1, -1) gives f(-1)f(1) = 0.
...
```

## Scope of version 1

* One unknown function f, with domain and codomain both R or both Q.
* Equations holding for all values of 2 or 3 variables, built from variables,
  rational constants, `+`, `-`, `*` and f applied to such expressions.
* Task: find **all** f.
* Answers are polynomial families with rational coefficients (`f(x) = cx + d`).
  A problem whose answer needs `sqrt(2)`, or has non-polynomial solutions
  (Cauchy's equation over R), is reported as unsolved, never answered wrongly.

Difficulty is measured on Evan Chen's MOHS scale (0M to 50M; 30M is a
medium-hard IMO problem). The target is 0-10M; 15-20M is a stretch goal.

### Future work (deliberately not built yet)

Positive-real domains, inequalities, integer or natural-number domains,
division, several unknown functions, continuity or monotonicity hypotheses.

## How it works

```
terms.py      expression trees, parser, printers            ┐
algebra.py    canonical polynomials with exact rationals    │ trusted core
solutions.py  solution families, exact parameter solving    │ (no floats,
checker.py    proof states, the moves, check(problem, proof)┘  no network)
moves.py      move data + text format
render.py     checked proof -> olympiad-style write-up
env.py        search environment (applies the routine "free" moves)
baseline/     answer guesser and brute-force search (the control experiment)
generate.py   synthetic problem generator and curriculum tiers
tokenizer.py  states and moves as tokens; grammar for constrained decoding
model.py      2.5M-parameter encoder-decoder transformer, policy + value heads
search.py     network-guided search: no backtracking / best-first
train.py      self-play training with hindsight examples and a curriculum
eval.py       three-mode evaluation, results tables
```

### The rule that cannot bend: soundness

The checker is exact code and the only trusted part. The network proposes,
the checker decides, and "solved" means the checker accepted every step of a
proof that was replayed from scratch. Arithmetic is exact (`fractions.Fraction`).
The classic traps are encoded and tested (`tests/test_traps.py`):

| trap | what the checker does |
|---|---|
| pointwise trap: "for every x, f(x) = 0 or f(x) = x" is not "f = 0 or f = x" | case splits only on facts without variables |
| cancelling f from f(A) = f(B) | only after injectivity has been established |
| choosing a with f(a) = t | only after surjectivity has been established, and only for constant t |
| dividing | only by constants proven nonzero; common factors need a case split |
| additive implies linear | only over Q, refused over R |
| case splits | factors are re-multiplied (exhaustive), and every case must close |
| claimed solutions | substituted back into the original equation exactly |

On top of that, a model-check fuzzer (`tests/test_modelcheck.py`,
`scripts/fuzz.py`) fires random moves at the checker and tests every accepted
state against known solutions of the benchmark problems.

### Proof state and moves

A proof state is a set of open *cases*. Each case holds identities (true for
all values of their variables), facts about constants, constants proven
nonzero, and proven properties (injective, surjective, odd, even, additive,
involution). The checker keeps the identities in a reduced form: adding,
subtracting and scaling identities, rewriting with known identities, and
applying proven properties all happen automatically, because each is a valid
deduction and none needs creativity (compare AlphaGeometry's deduction engine).

The moves, in the text format used by `alphafe check`:

```
sub P: x:=0, y:=f(y)       substitute into the original equation P
sub R2: x:=y               ... or into the 2nd current identity
sub [f(f(x)) = x]: x:=y+1  ... or into a quoted identity (must be known)
split [f(0)^2 = f(0)]      case split on a factorised fact about constants
splitnz f(0)               case split: f(0) = 0 or f(0) != 0
inj / surj                 establish injectivity / surjectivity
cancel                     f(A) = f(B) gives A = B (needs injectivity)
pre 0                      pick a with f(a) = 0 (needs surjectivity)
onto R2: y                 y occurs only as f(y) and f is surjective: replace f(y) by y
cauchy                     additive (up to a polynomial term) over Q implies polynomial
quadratic                  f(x+y) + f(x-y) = 2f(x) + 2f(y) over Q implies f(x) = f(1)x^2
conclude                   read off f(x) = ..., pin down constants by substituting back
div R3 by f(0)             divide by a proven-nonzero constant
```

A proof is a flat list of moves acting on the first open case. See
`benchmarks/seed/proofs/` for 48 worked examples (47 written by hand, one found by the network), and
`scripts/play.py` to step through a proof and see the state after each move.

### The network

The search environment applies the moves that need no creative input
(`conclude`, `cauchy`, `quadratic`, `inj`, `surj`, `cancel`) automatically. The network
chooses the rest: substitutions (writing the substituted term token by token,
there is no fixed pool), case splits, preimages. It reads the tokenised case
and writes a move under a grammar that only permits well-formed moves; a
value head estimates whether the state is solvable.

Training is self-play on synthetic problems, starting from random weights:
attempt problems, keep the proofs the checker accepts, and also learn from
failed attempts through hindsight (any identity that was derived is a correct
example of how to derive that identity). The curriculum moves to structurally
larger problems as the solve rate rises. The brute-force baseline is never
used to produce, label or filter training data.

## Benchmarks

* `benchmarks/seed/*.jsonl`: 50 classic easy problems written for this
  project (four of them in three variables), with expected answers (all
  verified) and estimated MOHS. It has been used to choose fixes, so treat it
  as a development set.
* `benchmarks/synthetic/heldout.jsonl`: 800 frozen held-out synthetic problems
  (200 per curriculum tier), never trained on.
* `benchmarks/real/`: empty; the owners add hand-picked problems there (format
  in its README) and `alphafe eval` picks them up automatically.
* The held-out split is about 10% of generated problems, chosen by a hash of
  the canonical equation. Training never sees it, the seed set or the real set.

## Honest limitations

* The checker's injectivity and surjectivity tests are syntactic patterns.
  A human can prove these properties in more ways than the checker recognises.
* There is no move for multiplying an identity by an expression, and products
  of f-values are only eliminated when they match exactly.
* The synthetic generator only produces two-variable problems. Three-variable
  problems are supported and tested (four seed problems), but the network has
  never trained on one.
* The network is small and each training run is about half an hour on a
  laptop GPU. See `RESULTS.md` for what is and is not solved, by which method,
  and how much of each comparison is within noise.
