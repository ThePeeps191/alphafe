"""Solution families, the small exact solver for parameter systems, and verification.

A *family* is an explicit formula ``f(x) = E`` where E is a polynomial in x
whose coefficients may involve free parameters, e.g. ``f(x) = c*x + d``.
A *solution set* is a finite list of families.

This module is trusted. It contains three things:

``solve_system``
    Solves polynomial systems in the parameters, but only by steps that are
    obviously exhaustive (solve a linear equation, enumerate rational roots,
    split a common factor). Anything else raises ``Unsupported`` rather than
    guessing, so "no solutions" always means no solutions.

``verify``
    Substitutes a family into the original equation and checks the result is
    identically zero.

``SolutionSet``
    A canonical form for answers so that two descriptions of the same set
    compare equal (``c*x`` versus ``2c*x``, a family listed twice, a family
    contained in another).
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Optional

from . import terms as T
from .algebra import (
    Poly,
    Unsupported,
    ZERO,
    apply_function,
    has_no_root,
    poly_str,
    rational_roots,
    split_by_vars,
    to_poly,
    univariate_coeffs,
)

X = ("v", "x")
PARAM_DISPLAY_NAMES = "cdkmnpqrs"


# ---------------------------------------------------------------------------
# Exact solver for polynomial systems in parameters
# ---------------------------------------------------------------------------

def _assign(polys: Iterable[Poly], atom, value: Poly) -> list[Poly]:
    mapping = {atom: value}
    return [p.replace_atoms(mapping) for p in polys]


def solve_system(equations: list[Poly], domain: str, _depth: int = 0) -> list[dict]:
    """Solve ``equations`` (each ``= 0``) for the named constants appearing in them.

    Returns a list of assignments ``{atom: Poly}``; the solution set of the
    system is exactly the union, over the returned assignments, of all points
    obtained by choosing the unassigned parameters freely. Every step keeps
    that "exactly":

    1. An equation ``q*c + rest = 0`` with q a nonzero rational and c not in
       ``rest`` is equivalent to ``c = -rest/q``.
    2. An equation in a single parameter c holds exactly at its roots. Rational
       roots are enumerated completely; we then need the remaining factor to
       have no root in the domain, otherwise the answer needs irrational
       constants and we raise ``Unsupported``.
    3. An equation ``c^k * rest = 0`` holds exactly when ``c = 0`` or ``rest = 0``.
    """
    if _depth > 24:
        raise Unsupported("parameter system too deep")
    eqs = []
    for eq in equations:
        if eq.is_zero():
            continue
        if eq.const_value() is not None:
            return []  # a nonzero number equals zero: no solutions
        if eq.variables() or any(a[0] != "c" for a in eq.top_atoms()):
            raise ValueError("solve_system expects polynomials in named constants only")
        if eq not in eqs:
            eqs.append(eq)
    if not eqs:
        return [{}]

    # Step 1: a linear equation.
    for eq in eqs:
        for atom in sorted(eq.top_atoms()):
            cs = eq.coeffs_in(atom)
            if set(cs) <= {0, 1} and 1 in cs:
                q = cs[1].const_value()
                if q is not None:
                    value = cs.get(0, ZERO).scale(-1 / q)
                    rest = [e for e in eqs if e is not eq]
                    out = []
                    for sol in solve_system(_assign(rest, atom, value), domain, _depth + 1):
                        resolved = value.replace_atoms(sol)
                        out.append({**sol, atom: resolved})
                    return out

    # Step 2: a univariate equation.
    for eq in eqs:
        uni = univariate_coeffs(eq)
        if uni is None:
            continue
        atom, coeffs = uni
        roots = rational_roots(coeffs)
        # Divide out the rational roots and make sure nothing else has a root.
        remaining = list(coeffs)
        for root in roots:
            while len(remaining) > 1 and sum(c * root**i for i, c in enumerate(remaining)) == 0:
                remaining = _synthetic_division(remaining, root)
        if len(remaining) > 1 and not has_no_root(remaining, domain):
            raise Unsupported("the answer would need irrational constants")
        rest = [e for e in eqs if e is not eq]
        out = []
        for root in roots:
            value = Poly.const(root)
            for sol in solve_system(_assign(rest, atom, value), domain, _depth + 1):
                out.append({**sol, atom: value})
        return out

    # Step 3: a common parameter factor.
    for eq in eqs:
        common = None
        for mono in eq.terms:
            exps = dict(mono)
            common = exps if common is None else {a: min(e, exps[a]) for a, e in common.items() if a in exps}
            if not common:
                break
        if common:
            atom = min(common)
            exp = common[atom]
            reduced = Poly({tuple((a, e - exp if a == atom else e) for a, e in mono if not (a == atom and e == exp)): c
                            for mono, c in eq.terms.items()})
            rest = [e for e in eqs if e is not eq]
            out = []
            for sol in solve_system(_assign(eqs, atom, ZERO), domain, _depth + 1):
                out.append({**sol, atom: ZERO})
            out.extend(solve_system(rest + [reduced], domain, _depth + 1))
            return out

    raise Unsupported("cannot solve the parameter system exactly")


def _synthetic_division(coeffs: list, root: Fraction) -> list:
    """Divide c0 + c1 t + ... by (t - root), assuming the division is exact."""
    out = [Fraction(0)] * (len(coeffs) - 1)
    carry = Fraction(0)
    for i in range(len(coeffs) - 1, 0, -1):
        carry = coeffs[i] + carry * root
        out[i - 1] = carry
    return out


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def verify(equation: Poly, expr: Poly) -> bool:
    """Does f(x) = ``expr`` satisfy ``equation = 0`` identically?

    ``expr`` may contain free parameters; the check then covers every value of
    the parameters at once, because the substituted equation must vanish as a
    polynomial in the variables *and* the parameters.
    """
    _check_family_expr(expr)
    return apply_function(equation, expr).is_zero()


def _check_family_expr(expr: Poly) -> None:
    for atom in expr.top_atoms():
        if atom[0] == "f":
            raise ValueError("a solution formula must not contain f")
        if atom[0] == "v" and atom != X:
            raise ValueError("a solution formula is written in the variable x")


def fit_candidate(equation: Poly, expr: Poly, domain: str) -> list[Poly]:
    """All members of the parametrised family ``expr`` that satisfy the equation.

    Substituting f(x) = expr turns the equation into a polynomial in the
    variables whose coefficients are polynomials in the parameters. It vanishes
    for all values of the variables exactly when every coefficient is zero
    (a polynomial over an infinite field that vanishes everywhere is the zero
    polynomial), which is a system ``solve_system`` can attack. Each resulting
    formula is verified again before being returned.
    """
    _check_family_expr(expr)
    residual = apply_function(equation, expr)
    system = list(split_by_vars(residual).values())
    out = []
    for assignment in solve_system(system, domain):
        solved = expr.replace_atoms(assignment)
        if not verify(equation, solved):
            raise AssertionError("internal error: solved family fails verification")
        out.append(solved)
    return out


# ---------------------------------------------------------------------------
# Canonical solution sets
# ---------------------------------------------------------------------------

def _x_coeffs(expr: Poly) -> list[Poly]:
    """Coefficients of 1, x, x^2, ... (polynomials in the parameters)."""
    cs = expr.coeffs_in(X)
    return [cs.get(i, ZERO) for i in range(max(cs, default=0) + 1)]


def _affine_parts(coeff: Poly, params: list) -> Optional[tuple]:
    """Write ``coeff`` as offset + sum(weight_i * param_i), or None if not affine."""
    offset = Fraction(0)
    weights = [Fraction(0)] * len(params)
    for mono, c in coeff.terms.items():
        if not mono:
            offset = c
        elif len(mono) == 1 and mono[0][1] == 1:
            weights[params.index(mono[0][0])] = c
        else:
            return None
    return offset, weights


def _rref(rows: list[list[Fraction]]) -> list[list[Fraction]]:
    """Reduced row echelon form, zero rows dropped. Pivots run from the *last*
    column to the first so that the first parameter multiplies the highest power of x."""
    rows = [list(r) for r in rows]
    out: list[list[Fraction]] = []
    ncols = len(rows[0]) if rows else 0
    for col in range(ncols - 1, -1, -1):
        pivot = next((r for r in rows if r[col] != 0), None)
        if pivot is None:
            continue
        rows.remove(pivot)
        pivot = [v / pivot[col] for v in pivot]
        rows = [[a - r[col] * b for a, b in zip(r, pivot)] for r in rows]
        out = [[a - r[col] * b for a, b in zip(r, pivot)] for r in out]
        out.append(pivot)
    return out


def _pivot_col(row: list[Fraction]) -> int:
    return max(i for i, v in enumerate(row) if v != 0)


def _reduce_vector(vec: list[Fraction], basis: list[list[Fraction]]) -> list[Fraction]:
    vec = list(vec)
    for row in basis:
        col = _pivot_col(row)
        if vec[col] != 0:
            factor = vec[col]
            vec = [a - factor * b for a, b in zip(vec, row)]
    return vec


@dataclass(frozen=True)
class Family:
    """One canonical family of solutions ``f(x) = expr``.

    ``affine`` is the canonical (offset, basis) description when the
    coefficients depend affinely on the parameters (the usual case); it is
    ``None`` for the rare non-affine family, which is then compared
    structurally after renaming parameters in order of appearance.
    """

    expr: Poly
    affine: Optional[tuple] = None

    @property
    def n_params(self) -> int:
        return len([a for a in self.expr.top_atoms() if a[0] == "c"])

    def contains(self, other: "Family") -> bool:
        """Is every function of ``other`` also in this family? (Sound but not
        complete for non-affine families.)"""
        if self.expr == other.expr:
            return True
        if self.affine is None and other.n_params == 0:
            # Is the single function ``other`` a member? Solve for the parameters.
            mine, theirs = _x_coeffs(self.expr), _x_coeffs(other.expr)
            width = max(len(mine), len(theirs))
            system = [(mine[i] if i < len(mine) else ZERO) - (theirs[i] if i < len(theirs) else ZERO)
                      for i in range(width)]
            try:
                return bool(solve_system(system, "R"))
            except Unsupported:
                return False
        if self.affine is None or other.affine is None:
            return False
        width = max(len(self.affine[0]), len(other.affine[0]))
        pad = lambda v: list(v) + [Fraction(0)] * (width - len(v))
        basis = [pad(b) for b in self.affine[1]]
        diff = [a - b for a, b in zip(pad(other.affine[0]), pad(self.affine[0]))]
        if any(_reduce_vector(diff, basis)):
            return False
        return all(not any(_reduce_vector(pad(b), basis)) for b in other.affine[1])

    def __str__(self) -> str:
        return f"f(x) = {poly_str(self.expr)}"

    def describe(self) -> str:
        params = sorted(a[1] for a in self.expr.top_atoms() if a[0] == "c")
        if not params:
            return str(self)
        noun = "constant" if len(params) == 1 else "constants"
        return f"{self} for any {noun} {', '.join(params)}"


def _absorb_free_coefficients(expr: Poly) -> Poly:
    """Simplify parameters that make a whole coefficient free.

    If a parameter p occurs in the formula exactly once, as a lone term q*p
    inside the coefficient of one power of x, then as p ranges over all
    numbers so does that coefficient, whatever the other parameters are. The
    coefficient can therefore be replaced by a single fresh parameter:
    ``x^2 - a^2 + b`` describes the same functions as ``x^2 + c``.
    """
    xp = Poly.atom(X)
    for _ in range(20):
        coeffs = _x_coeffs(expr)
        counts: dict = {}
        for coeff in coeffs:
            for mono in coeff.terms:
                for atom, exp in mono:
                    counts[atom] = counts.get(atom, 0) + (1 if len(mono) == 1 and exp == 1 else 2)
        for i, coeff in enumerate(coeffs):
            if len(coeff.terms) < 2:
                continue
            lone = [mono[0][0] for mono in coeff.terms if len(mono) == 1 and counts.get(mono[0][0]) == 1]
            if lone:
                fresh = Poly.named(f"#free{i}_{len(counts)}")
                expr = expr - coeff * xp ** i + fresh * xp ** i
                break
        else:
            return expr
    return expr


def make_family(expr: Poly) -> Family:
    """Canonicalise a formula: rename and reduce its parameters."""
    _check_family_expr(expr)
    expr = _absorb_free_coefficients(expr)
    params = sorted(a for a in expr.top_atoms() if a[0] == "c")
    coeffs = _x_coeffs(expr)
    parts = [_affine_parts(c, params) for c in coeffs]
    xp = Poly.atom(X)
    if all(p is not None for p in parts):
        offset = [p[0] for p in parts]
        rows = [[p[1][i] for p in parts] for i in range(len(params))]
        basis = _rref(rows) if rows else []
        offset = _reduce_vector(offset, basis)
        canonical = ZERO
        for i, value in enumerate(offset):
            canonical = canonical + (xp ** i) * value
        for j, row in enumerate(basis):
            name = Poly.named(PARAM_DISPLAY_NAMES[j])
            for i, value in enumerate(row):
                canonical = canonical + name * (xp ** i) * value
        while offset and offset[-1] == 0 and all(r[len(offset) - 1] == 0 for r in basis):
            offset = offset[:-1]
            basis = [r[:-1] for r in basis]
        return Family(canonical, (tuple(offset), tuple(tuple(r) for r in basis)))
    # Non-affine: rename parameters in order of first appearance.
    renaming = {}
    for mono, _ in expr.key:
        for atom, _ in mono:
            if atom[0] == "c" and atom not in renaming:
                renaming[atom] = Poly.named(PARAM_DISPLAY_NAMES[len(renaming)])
    return Family(expr.replace_atoms(renaming), None)


@dataclass(frozen=True)
class SolutionSet:
    """A canonical, order-independent set of families."""

    families: tuple

    def __str__(self) -> str:
        if not self.families:
            return "no solutions"
        return "; ".join(f.describe() for f in self.families)

    def __len__(self) -> int:
        return len(self.families)

    def contains_function(self, expr: Poly) -> bool:
        """Is the parameter-free function f(x) = expr a member of the set?"""
        single = make_family(expr)
        return any(fam.contains(single) for fam in self.families)


def make_solution_set(exprs: Iterable[Poly]) -> SolutionSet:
    families: list[Family] = []
    for expr in exprs:
        fam = make_family(expr)
        if any(existing.contains(fam) for existing in families):
            continue
        families = [existing for existing in families if not fam.contains(existing)]
        families.append(fam)
    families.sort(key=lambda fam: (fam.n_params, fam.expr.key))
    return SolutionSet(tuple(families))


def parse_solution(text: str) -> Poly:
    """Parse ``f(x) = c*x + d`` into the polynomial on the right-hand side."""
    lhs, rhs = T.parse_equation(text)
    if lhs != T.App(T.Var("x")):
        raise T.ParseError("a solution is written as f(x) = ...")
    expr = to_poly(rhs)
    try:
        _check_family_expr(expr)
    except ValueError as err:
        raise T.ParseError(str(err)) from None
    return expr


def parse_solution_set(texts: Iterable[str]) -> SolutionSet:
    return make_solution_set(parse_solution(t) for t in texts)
