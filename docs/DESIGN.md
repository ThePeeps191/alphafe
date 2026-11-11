# How AlphaFE works

Reference material for the proof format, the checker and the network. The
README has the short version; `docs/EXTENDING.md` covers adding a move or
running an experiment.

## Modules

```
terms.py      expression trees, parser, printers            ┐
algebra.py    canonical polynomials with exact rationals    │ trusted core
solutions.py  solution families, exact parameter solving    │ (no floats,
checker.py    proof states, the moves, check(problem, proof)┘  no network)
moves.py      move data and text format
render.py     checked proof to olympiad-style write-up
env.py        search environment (applies the routine moves)
baseline/     answer guesser and brute-force search
generate.py   synthetic problem generator and curriculum tiers
tokenizer.py  states and moves as tokens; grammar for constrained decoding
model.py      2.5M-parameter encoder-decoder transformer, policy and value heads
search.py     network-guided search, with and without backtracking
train.py      self-play training with hindsight examples and a curriculum
eval.py       evaluation and results tables
bench.py      benchmark loading and the answer check
```

## Proof states

A proof state is a set of open cases. Each case holds:

* identities, which are true for all values of their variables;
* facts about constants such as `f(0)`;
* constants proven nonzero;
* proven properties of f: injective, surjective, odd, even, additive, involution.

The checker keeps the identities in a reduced form. Adding, subtracting and
scaling identities, rewriting one identity with another, and applying proven
properties all happen automatically, because each is a valid deduction that
takes no idea to find. This plays the part of AlphaGeometry's deduction engine.

## Moves

A proof is a list of moves, one per line, each acting on the first open case.
`#` starts a comment.

```
sub P: x:=0, y:=f(y)       substitute into the original equation P
sub R2: x:=y               substitute into the 2nd current identity
sub [f(f(x)) = x]: x:=y+1  substitute into a quoted identity (must be known)
split [f(0)^2 = f(0)]      case split on a factorised fact about constants
splitnz f(0)               case split: f(0) = 0 or f(0) != 0
inj                        establish injectivity
surj                       establish surjectivity
cancel                     f(A) = f(B) gives A = B (needs injectivity)
pre 0                      pick a with f(a) = 0 (needs surjectivity)
onto R2: y                 y occurs only as f(y) and f is surjective: replace f(y) by y
cauchy                     additive (up to a polynomial term) over Q implies polynomial
quadratic                  f(x+y) + f(x-y) = 2f(x) + 2f(y) over Q implies f(x) = f(1)x^2
sqadd                      f(x^2 + y) = f(x^2) + f(y), or over R f(x^2 - y^2) = f(x^2) - f(y^2),
                           implies f is additive
sqlin                      over R: additive with f(x^2) = f(x)^2 implies f(x) = f(1)x
conclude                   read off f(x) = ..., pin down constants by substituting back
div R3 by f(0)             divide by a proven-nonzero constant
```

`benchmarks/seed/proofs/` has 49 examples (48 written by hand, one found by
the network). `scripts/play.py` steps through a proof and prints the state
after each move.

## Soundness

Only the checker is trusted. The network proposes moves and the checker
decides; a problem counts as solved when the checker has accepted every step
of a proof replayed from the original equation. All arithmetic uses
`fractions.Fraction`.

The standard mistakes in functional-equation proofs are each blocked by a
rule and covered in `tests/test_traps.py`:

| mistake | rule in the checker |
|---|---|
| reading "for every x, f(x) = 0 or f(x) = x" as "f = 0 or f = x" | case splits are allowed only on facts without variables |
| cancelling f from f(A) = f(B) | allowed only after injectivity is established |
| choosing a with f(a) = t | allowed only after surjectivity is established, and only for constant t |
| dividing | allowed only by constants proven nonzero; a common factor needs a case split |
| concluding that an additive f is linear | allowed over Q; over R only together with f(x^2) = f(x)^2, which makes f monotone (`sqlin`) |
| treating "additive on squares" as additive | `sqadd` needs f(x^2 + y) = f(x^2) + f(y) with a free y; f(x^2 + y^2) = f(x^2) + f(y^2) holds for f(t) = \|t\| and is refused |
| using "every non-negative number is a square" over Q | the difference-of-squares form of `sqadd` is refused over Q |
| incomplete case splits | the factors are multiplied back to confirm the split is exhaustive, and every case must close |
| unverified answers | every claimed solution is substituted into the original equation exactly |

Two further checks run outside the proof rules. A fuzzer
(`tests/test_modelcheck.py`, `scripts/fuzz.py`) applies random moves and tests
every accepted state against known solutions of the benchmark problems. And
whenever a benchmark problem has a recorded answer, a proof that produces a
different answer raises `AnswerMismatch` instead of being scored.

## The network

The search environment (`alphafe/env.py`) does two things by itself after
every proposed move.

It applies the free moves `conclude`, `cauchy`, `quadratic`, `sqadd`,
`sqlin`, `inj`, `surj` and `cancel` whenever they are legal.

It then applies routine substitutions, which are ordinary `sub` moves that
need no idea:

* at the start, the opening substitutions into the original equation P:
  `x:=0, y:=0`, `x:=0`, `y:=0`, `y:=x` and `y:=-x`;
* the swap `x:=y, y:=x` of a two-variable problem;
* closed instances: an identity in one variable v taken at v := T, where T
  is 0 or the argument of an f(...) already present, provided the result
  mentions no f(...) that is not present already. Without that condition
  the step feeds itself and never stops;
* a witness named by `pre` put into P, one variable at a time.

Each of these goes through the checker and is written into the proof like
any other move, so they cannot make the checker accept more. Knowledge in a
case only grows, so applying them eagerly cannot lose a proof. It costs
time: a proposed move takes several times longer to process. At most ten
are applied after one proposed move. `env.ROUTINE` switches each kind off,
for measuring and for tests.

Found proofs therefore contain many moves that the final argument does not
use. `env.minimise` drops proposed moves that are not needed and then
`env.prune` removes every single move the proof can do without, as judged by
re-checking; numbered targets are first rewritten as quoted identities so
that removing an earlier move does not change what a later one points at.

The network (or brute force) chooses the remaining moves: substitutions that
need an idea, case splits and preimages. It reads the
tokenised case and writes the move token by token, so a substituted term can
be any expression and is not picked from a fixed list. A grammar restricts
the output to well-formed moves. A value head estimates whether the state is
solvable. Sampling decodes one position at a time from cached attention keys
and values (`model.StepDecoder`).

A search with backtracking asks for eight proposals per state. Six are
sampled from the network. Two are built from the page
(`tokenizer.sample_subterm_move`): a substitution whose term is an expression
that already occurs in the state, as it is, negated, or added to the
variable. A trained policy gives whole kinds of move almost no probability
(`x := f(x)` is the usual example), and sampling it more often does not find
them; these two proposals do. The brute-force pool is not involved.

Training is self-play on synthetic problems from random weights. The network
attempts problems, and the proofs the checker accepts become training
examples. Failed attempts are used too: any identity derived along the way is
a correct example of how to derive that identity (hindsight).

Which problems are attempted next is decided by a curriculum. `tiers` moves
to structurally larger problems as the solve rate rises. `adaptive` has no
ladder: every problem can be drawn from the start, with a weight from its own
history (untried 1, unsolved 1 / (1 + failures), solved 0.5 / sqrt(1 + times
solved)), so the order of difficulty is found and not assumed.

With `workers=N` self-play runs in N processes, each with the current weights
on one CPU core, while the gradient steps run on the GPU. The checker is the
slow part of self-play and the network is small enough to propose moves on a
CPU core.

The brute-force baseline is the control experiment. It is never used to
produce, label or filter training data, and `tests/test_isolation.py` checks
that the training modules do not import it.

## Size limits

The checker refuses work it would have to refuse the result of anyway. None
of these is a soundness rule; each turns "too large" into a refused move.

| limit | value | what it bounds |
|---|---|---|
| `MAX_POLY_TERMS`, `MAX_POLY_SIZE` | 80, 400 | monomials and structural size of one identity |
| `MAX_ROWS` | 40 | identities in one case |
| `MAX_TERM_SIZE` | 40 | nodes of a term written in a move |
| `WORK_TERMS` | 1,000 | term pairs in one multiplication, and terms held, while a substitution is expanded |
| `env.INSTANCE_WORK` | 200 | the same, for the environment's routine instances |
| `env.MAX_ROUTINE` | 10 | routine substitutions applied after one proposed move |

## Speed

The search inner loop is the checker, so three things are cached. All three
are exact: the same proofs come out with and without them.

* An atom `f(p)` is an `algebra.FAtom`: a tuple that stores its hash, shared
  between equal atoms, and that keeps its argument as a polynomial.
* A polynomial remembers its leading monomial, its variables and its
  top-level atoms.
* The environment keeps the normal form of each routine instance together
  with what it depended on: the properties in force and, for every atom that
  was looked up, the rule it had. It is reused only while all of that holds.

## Limits of the checker and generator

* Injectivity and surjectivity are recognised by syntactic patterns. A person
  can prove these properties in more ways than the checker accepts.
* No move multiplies an identity by an expression, and products of f-values
  are eliminated only when they match exactly.
* The synthetic generator produces two-variable problems only. Three-variable
  problems are supported and tested on four seed problems, but the network
  has never trained on one.
* Answers are polynomial families with rational coefficients. A problem whose
  answer needs `sqrt(2)`, or that has non-polynomial solutions (Cauchy's
  equation over R), is reported as unsolved.
