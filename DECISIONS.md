# Decisions

One line (or a short paragraph) per choice, newest at the bottom.

- **Environment**: Python 3.12 in a project-local `.venv` created with `uv`; nothing installed globally (owner's rule).
- **Dependencies**: torch at runtime; pytest, hypothesis, sympy for tests only. No numpy (torch prints a harmless warning without it, filtered in pytest).
- **Symbol classes**: variables are `x y z t u v w` (universally quantified, substitutable); every other lowercase letter except `f` is a named constant (a witness in a proof, a parameter in an answer) and can never be substituted for.
- **Division in the input language**: only by an integer literal (`x/2`), which is how rational constants are written. Division by expressions is out of scope for v1.
- **Canonical form**: polynomials with `Fraction` coefficients over atoms (variable, named constant, or f(canonical polynomial)), stored as dicts keyed by sorted monomial tuples. Written from scratch; SymPy is used only in tests.
- **Leading monomial**: identities are solved for their most complicated monomial, ranked by (nesting depth of f over variables, structural size, canonical order). See `algebra.mono_rank`.
- **Network term syntax**: prefix (Polish) notation, so constrained decoding only has to count owed operands. Integers above 20 collapse to one lossy token `N` in states.
- **Proof state = reduced identities**: each branch keeps its identities in reduced echelon form over Q (every identity solved for its leading monomial). Adding, subtracting and scaling identities therefore happens automatically inside the checker rather than as explicit moves; an explicit "combine" move could never add information. Swapping variables is a substitution (`sub P: x:=y, y:=x`).
- **Rewriting is automatic**: an identity whose leading monomial is a single atom is used as a rewrite rule everywhere, including inside f(...) (congruence). So "rewrite using a known identity" is not a separate move either; to rewrite with an *instance* of an identity, substitute into it first.
- **Properties are flags with their own rewriting**: odd, even, additive, involution are recognised from their defining identity and then applied to every matching f(...). Involution also sets injective and surjective.
- **One-variable identities are renamed automatically** to the other variables in use (an identity for all x is an identity for all y).
- **Flat proofs, depth-first cases**: a proof is a flat list of moves acting on the first open case; a split replaces the current case by its sub-cases. Facts are branch-local by construction (each case is its own object).
- **Case splits**: only on variable-free facts, with factors re-multiplied by the checker (`split`), or `c = 0` versus `c != 0` for a constant c (`splitnz`). The factoring helper is untrusted; the multiplication check is what counts.
- **Injectivity/surjectivity** are established by syntactic criteria (see `checker.injectivity_variable`, `surjectivity_variable`), not by sub-proofs. Narrower than what a human can do, but easy to trust.
- **Preimages** (`pre t`) only for constant targets t; the witness is a named constant and can never be substituted for. The separate move `onto` covers "f(y) takes every value" when y occurs only inside f(y).
- **Conclude = read off + pin down + verify**: `conclude` takes an identity f(a*x + b) = E, replaces every unknown constant in E by a free parameter, substitutes into the *original* equation and solves the coefficient system exactly. Verification of candidate solutions is part of this move (and repeated in `check`), not a separate proof move; `checker.verify_solution` exposes it on its own.
- **Exact parameter solving only**: `solutions.solve_system` solves linear equations, enumerates rational roots and splits common factors; anything else raises `Unsupported` and the move is rejected. Consequence: answers needing irrational constants (f(x) = sqrt(2) x) are out of reach in v1 and are reported as unsolved, never as "no solutions".
- **"No new information" is a rejection**: a legal move that changes nothing is refused, so proofs have no dead steps and search can prune.
- **Answer comparison**: solution sets are canonicalised (affine families via row reduction, lone free parameters absorbed). Known limitation: two different non-affine parametrisations of the same set (e.g. `a*b*x` vs `c*x`) are not recognised as equal.
- **Extra move `div`**: explicit division by a proven-nonzero constant exists mainly so the "divide by something not proven nonzero" trap can be tested; the normaliser performs legal divisions itself.
- **Size caps** (rows per case, monomials per identity, term size, open cases) reject moves that blow up. They limit what can be proven, never what is sound.
- **Model-check fuzzing** (`alphafe/modelcheck.py`, `tests/test_modelcheck.py`, `scripts/fuzz.py`): random accepted moves are tested against known solutions of the seed problems. It is a test tool and is never used to accept a proof.
