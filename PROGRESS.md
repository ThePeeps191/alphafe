# Progress

A fresh session should read this file, `DECISIONS.md` and `git log` first.

## Done

- **M0 scaffold**: `pyproject.toml`, package `alphafe/`, pytest, `.gitignore`, docs.
- **M1 terms and algebra**: `alphafe/terms.py` (expression trees, infix parser and
  printer, prefix serialisation) and `alphafe/algebra.py` (canonical polynomials,
  substitution, deep rewriting, exact division, rational roots, factoring hints,
  evaluation). Property tests and a SymPy cross-check in `tests/`.

## Next

- **M2 checker, moves, renderer** (`alphafe/checker.py`, `moves.py`, `render.py`),
  seed benchmark with at least 15 hand-written proofs, wrong-proof suite.
- M3 baseline guesser + brute force; M4 generator/tokenizer/model/training; M5; M6.

## How to run

```sh
.venv/bin/python -m pytest          # all tests
```

## Known problems

- None yet.
