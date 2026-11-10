# Decisions

One line (or a short paragraph) per choice, newest at the bottom.

- **Environment**: Python 3.12 in a project-local `.venv` created with `uv`; nothing installed globally (owner's rule).
- **Dependencies**: torch at runtime; pytest, hypothesis, sympy for tests only. No numpy (torch prints a harmless warning without it, filtered in pytest).
- **Symbol classes**: variables are `x y z t u v w` (universally quantified, substitutable); every other lowercase letter except `f` is a named constant (a witness in a proof, a parameter in an answer) and can never be substituted for.
- **Division in the input language**: only by an integer literal (`x/2`), which is how rational constants are written. Division by expressions is out of scope for v1.
- **Canonical form**: polynomials with `Fraction` coefficients over atoms (variable, named constant, or f(canonical polynomial)), stored as dicts keyed by sorted monomial tuples. Written from scratch; SymPy is used only in tests.
- **Leading monomial**: identities are solved for their most complicated monomial, ranked by (nesting depth of f over variables, structural size, canonical order). See `algebra.mono_rank`.
- **Network term syntax**: prefix (Polish) notation, so constrained decoding only has to count owed operands. Integers above 20 collapse to one lossy token `N` in states.
