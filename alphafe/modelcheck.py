"""Model checking: test proof states against a function known to solve the problem.

Not part of the checker and never used to accept a proof. It is a testing
tool: if F really satisfies the equation, then in every case branch whose
assumptions F fulfils, every derived identity must hold for F, every claimed
property must be true of F, and F must never be "lost" (it must stay in some
open branch or appear among the reported solutions). Any violation means some
move is unsound.
"""

from __future__ import annotations

import random
from fractions import Fraction
from typing import Optional

from .algebra import Poly, evaluate
from .checker import Branch, State
from .solutions import make_solution_set

X = ("v", "x")


class Unsound(AssertionError):
    """A proof state contradicts a known solution."""


def _degree(expr: Poly) -> int:
    return max(expr.coeffs_in(X), default=0)


def _function(expr: Poly):
    return lambda t: evaluate(expr, None, {"x": t})


def branch_environment(branch: Branch, expr: Poly):
    """Values of the witnesses under which f = expr fulfils the branch assumptions.

    Returns a dict (possibly empty) if f belongs to this branch, ``None`` if it
    does not, and the string ``"unknown"`` if we cannot tell (a witness for a
    function whose preimages we do not compute).
    """
    func = _function(expr)
    env: dict = {}
    degree = _degree(expr)
    for assumption in branch.assumptions:
        kind = assumption[0]
        if kind == "witness":
            _, name, target = assumption
            value = evaluate(target, func, env)
            if degree == 1:
                coeffs = expr.coeffs_in(X)
                slope = coeffs[1].const_value()
                intercept = coeffs.get(0, Poly()).const_value()
                env[name] = (value - intercept) / slope
            elif degree in (0, 2):
                # f fulfilled everything assumed so far, yet surjectivity was
                # "proven": constants and quadratics are not surjective.
                raise Unsound(f"surjectivity was established but f(x) = {expr} is not surjective")
            else:
                return "unknown"
        else:
            value = evaluate(assumption[1], func, env)
            if (kind == "zero") != (value == 0):
                return None
    return env


def check_branch(branch: Branch, expr: Poly, rng: random.Random, samples: int = 3) -> Optional[bool]:
    """Raise ``Unsound`` if the branch claims something false about f = expr.

    Returns True if the branch applies to f, False if not, None if unknown.
    """
    env = branch_environment(branch, expr)
    if env is None:
        return False
    if env == "unknown":
        return None
    func = _function(expr)
    degree = _degree(expr)

    def point():
        values = dict(env)
        for name in "xyztuvw":
            values[name] = Fraction(rng.randint(-6, 6), rng.randint(1, 3))
        return values

    for _ in range(samples):
        values = point()
        for row in branch.rows:
            if evaluate(row, func, values) != 0:
                raise Unsound(f"identity {row} = 0 fails for f(x) = {expr} at {values}")
        for known in branch.nonzero:
            if evaluate(known, func, values) == 0:
                raise Unsound(f"{known} is claimed nonzero but vanishes for f(x) = {expr}")
        s, t = values["x"], values["y"]
        claims = {
            "odd": func(-s) == -func(s),
            "even": func(-s) == func(s),
            "additive": func(s + t) == func(s) + func(t),
            "involution": func(func(s)) == s,
        }
        for prop, holds in claims.items():
            if prop in branch.props and not holds:
                raise Unsound(f"f is claimed {prop} but f(x) = {expr} is not")
    if degree in (0, 2):
        for prop in ("injective", "surjective"):
            if prop in branch.props:
                raise Unsound(f"f is claimed {prop} but f(x) = {expr} is not")
    return True


def check_state(state: State, expr: Poly, rng: random.Random) -> None:
    """Raise ``Unsound`` if ``state`` contradicts the known solution f = expr."""
    statuses = [check_branch(branch, expr, rng) for branch in state.branches]
    if any(status is True or status is None for status in statuses):
        return
    if not make_solution_set(state.solutions).contains_function(expr):
        raise Unsound(f"the solution f(x) = {expr} was lost: it is in no open case and not among the solutions")
