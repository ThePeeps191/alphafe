# AlphaFE

A solver for easy olympiad **functional equations**, for example

> Find all f: R -> R with f(x + y) = f(x) + y for all real x, y.

The design follows [AlphaGeometry](https://www.nature.com/articles/s41586-023-06747-5):
an exact symbolic checker defines the legal proof moves, and a small neural
network, trained from scratch on its own attempts, decides which moves to make.
AlphaGeometry is the inspiration; this is an independent hobby project by two
olympiad students and is not affiliated with DeepMind.

**Status: under construction.** See `PROGRESS.md` for what works today,
`DECISIONS.md` for design choices and `RESULTS.md` for measured results.

## Setup

Everything lives in a project virtual environment (nothing is installed globally):

```sh
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python -e ".[dev]"
.venv/bin/python -m pytest
```

## Scope of version 1

* One unknown function f, with domain and codomain both R or both Q.
* Equations holding for all values of 2 or 3 variables, built from variables,
  rational constants, `+`, `-`, `*` and f applied to such expressions.
* Task: find **all** f, with a checked proof that the listed functions work and
  nothing else does.

Difficulty is measured on Evan Chen's MOHS scale. The target is 0-10M problems
(3-6 standard moves); 15-20M is a stretch goal.

### Future work (deliberately not built yet)

Positive-real domains, inequalities, integer or natural-number domains,
division, several unknown functions, continuity or monotonicity hypotheses.
