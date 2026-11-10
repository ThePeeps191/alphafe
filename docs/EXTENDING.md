# Extending AlphaFE

Notes for whoever picks this up next. Read `README.md` first.

## A tour through one proof

```sh
.venv/bin/python scripts/play.py "f(x)f(y) = f(x+y) + xy" R benchmarks/seed/proofs/s33.proof
```

prints the state after every move: the open cases, the proven properties and
the current identities `R1, R2, ...`. This is the fastest way to understand
what the checker's automatic normalisation does, and the tool to use when
writing a proof by hand.

## Adding a move to the checker

The checker is the trusted core, so the order matters.

1. **Write the maths down first**, as the docstring of the handler you are
   about to write: what is assumed, what is concluded, and why it is true for
   *every* function satisfying the current facts. If you cannot write that
   paragraph, the move is not ready.
2. **Write the tests first** (`tests/test_checker.py` or a new file): one
   proof that needs the move, and the cases where it must be refused.
3. **Add a trap test** to `tests/test_traps.py` if the move has a classic way
   of being misused (most do).
4. Implement: a dataclass and text syntax in `alphafe/moves.py`, a handler
   `_do_<name>` in `alphafe/checker.py`, an entry in `_HANDLERS`, a sentence
   in `alphafe/render.py`.
5. **Fuzz it.** Add the move to `random_move` in `tests/test_modelcheck.py`
   and run `scripts/fuzz.py 80 100` and `scripts/fuzz_synthetic.py 400 80 4`.
   The fuzzer checks every accepted state against known solutions; it found
   one real bug during development (in the answer canonicaliser).
6. If the move needs no creative input, add it to `FREE_MOVES` in
   `alphafe/env.py`. If the network should choose it, add tokens and grammar
   states in `alphafe/tokenizer.py` (and expect to retrain).
7. Run `scripts/check_seed_proofs.py`: every stored proof must still check.

Things that are easy to get wrong:

* An identity is "for all values of its variables". A fact about one value of
  x is a fact about a *constant*; do not let it turn into an identity.
* Anything that picks one of several possibilities (a root, a sign, a factor)
  must become a case split on a constant, never a silent choice.
* "No solutions" must mean exactly that. When the exact machinery cannot
  decide, raise `Unsupported` or reject the move; never return an empty answer.
* Automatic steps in `Branch.add` run on every identity. A step that is
  valid "usually" is a soundness bug.

## Adding problems

* Seed problems: a line in `benchmarks/seed/*.jsonl` and, if you can, a proof
  in `benchmarks/seed/proofs/<id>.proof`. `tests/test_checker.py` verifies
  every recorded answer by substitution and every stored proof.
* Real problems: drop a `.jsonl` file into `benchmarks/real/` (format in its
  README). `alphafe eval` picks it up. If a checked proof ever disagrees with
  a recorded answer, evaluation stops with `AnswerMismatch`: one of the two is
  wrong, and it is worth finding out which.
* Never train on either. The generator excludes them by canonical hash.

## Running an experiment

1. Change one thing. Commit it.
2. Train: `alphafe train --run NAME --minutes 28` (add `--resume` to continue).
3. Evaluate at a fixed commit: `alphafe eval --checkpoint checkpoints/NAME/last.pt --tag NAME --seeds 3`.
   Do not edit `alphafe/` while it runs.
4. Compare against another checkpoint evaluated at the *same* commit.
5. Write it up in `RESULTS.md`: what changed, the commit, the numbers, and
   whether the difference is larger than the spread over sampling seeds.
   Include it when it did not help.

Useful scripts: `scripts/show_log.py` (training curve),
`scripts/analyse_failures.py` (sort seed failures into the three groups),
`scripts/diagnose.py` (how likely the network finds each move of a known proof).

## Where the limits are

See "Honest limitations" in the README and the last section of `RESULTS.md`.
The checker rejects anything it cannot justify, so most limits show up as
"not solved" rather than as wrong answers; that is by design.
