"""Solutions that are not polynomials, as test models for the checker.

"Solved" claims that there are no solutions besides the listed polynomial
families. The mistake that claim most needs protecting from is closing every
case while a non-polynomial function still satisfies the equation: |x| for
f(x)^2 = x^2, or a wild additive function for Cauchy's equation over R. The
polynomial models of ``alphafe.modelcheck`` cannot see such a mistake, because
such a function is never one of them.

Here a model is a Python function with what is known about it. Wild additive
functions are modelled exactly on Q(sqrt 2): the numbers a + b*sqrt(2) with a
and b rational are real numbers, and conjugation a + b*sqrt(2) -> a - b*sqrt(2)
is additive there (it extends to an additive function on all of R), fixes the
rationals and is not linear.

``walk`` fires random moves at the checker. After every accepted move the
model must still fulfil the assumptions of at least one open case, every
identity of such a case must vanish for it at random points, no property
claimed there may be false of it, and the state must not be solved.

Used by tests/test_nonpoly.py and scripts/fuzz.py. Nothing here is part of
the checker.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, Optional

from alphafe.algebra import Poly, atom_arg
from alphafe.checker import Problem, Reject, apply, initial_state
from alphafe.env import close
from alphafe.modelcheck import Unsound


class S2:
    """The real number a + b*sqrt(2), with a and b rational. Exact."""

    __slots__ = ("a", "b")

    def __init__(self, a, b=0):
        self.a, self.b = Fraction(a), Fraction(b)

    @staticmethod
    def of(value) -> "S2":
        return value if isinstance(value, S2) else S2(value)

    def __add__(self, other):
        other = S2.of(other)
        return S2(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return S2(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-S2.of(other))

    def __rsub__(self, other):
        return S2.of(other) - self

    def __mul__(self, other):
        other = S2.of(other)
        return S2(self.a * other.a + 2 * self.b * other.b, self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = S2.of(other)
        norm = other.a ** 2 - 2 * other.b ** 2          # nonzero unless other is 0: sqrt(2) is irrational
        return self * S2(other.a / norm, -other.b / norm)

    def __rtruediv__(self, other):
        return S2.of(other) / self

    def __pow__(self, exponent: int):
        result = S2(1)
        for _ in range(exponent):
            result = result * self
        return result

    def __eq__(self, other):
        if not isinstance(other, (S2, Fraction, int)):
            return NotImplemented
        other = S2.of(other)
        return self.a == other.a and self.b == other.b

    def __hash__(self):
        return hash((self.a, self.b))

    def __repr__(self):
        return f"({self.a} + {self.b}*sqrt2)"


def value(poly: Poly, fn: Callable, values: dict):
    """``poly`` with f := fn and the given values of the variables and named constants. Any exact number type."""
    total = Fraction(0)
    for mono, coef in poly.terms.items():
        product = coef
        for atom, exp in mono:
            factor = fn(value(atom_arg(atom), fn, values)) if atom[0] == "f" else values[atom[1]]
            product = product * factor ** exp
        total = total + product
    return total


def rational_point(rng: random.Random):
    return Fraction(rng.randint(-7, 7), rng.randint(1, 3))


def s2_point(rng: random.Random):
    return S2(Fraction(rng.randint(-5, 5), rng.randint(1, 2)), Fraction(rng.randint(-4, 4), rng.randint(1, 2)))


@dataclass
class Model:
    """A function that solves an equation, with what is true of it."""

    name: str
    fn: Callable
    injective: bool = False
    surjective: bool = False
    preimage: Optional[Callable] = None       # for a surjective model: some t with fn(t) = the argument
    point: Callable = rational_point          # where its identities are tested


def _conjugate(t):
    t = S2.of(t)
    return S2(t.a, -t.b)


def _inverse(t):
    return Fraction(0) if t == 0 else 1 / t


def _swap01(t):
    return Fraction(1) if t == 0 else Fraction(0) if t == 1 else t


ABS = Model("|x|", abs)
SIGN = Model("sign", lambda t: Fraction((t > 0) - (t < 0)))
NONZERO = Model("1 for x != 0, 0 at 0", lambda t: Fraction(t != 0))
INVERSE = Model("1/x, 0 at 0", _inverse, injective=True, surjective=True, preimage=_inverse)
SWAP01 = Model("swap 0 and 1", _swap01, injective=True, surjective=True, preimage=_swap01)
POSITIVE_PART = Model("max(x, 0)", lambda t: max(t, Fraction(0)))
FLOOR = Model("floor", lambda t: Fraction(math.floor(t)))
UNIT = Model("x if |x| = 1, else 0", lambda t: t if abs(t) == 1 else Fraction(0))
CONJUGATION = Model("conjugation on Q(sqrt 2)", _conjugate, injective=True, surjective=True, preimage=_conjugate,
                    point=s2_point)
RATIONAL_PART = Model("rational part on Q(sqrt 2)", lambda t: S2(S2.of(t).a), point=s2_point)
NORM = Model("norm a^2 - 2b^2 on Q(sqrt 2)", lambda t: S2(S2.of(t).a ** 2 - 2 * S2.of(t).b ** 2), point=s2_point)
SQUARE_OF_CONJUGATE = Model("square of the conjugate", lambda t: _conjugate(t) ** 2, point=s2_point)

# (equation, domain, model). Each model satisfies its equation on the stated domain (the test checks this at
# random points first), and none is a polynomial. Over Q the equations of the last block have only
# polynomial solutions, which is the whole point of running them over R.
CASES = [
    ("f(xy) = f(x)f(y)", "R", ABS),
    ("f(xy) = f(x)f(y)", "Q", ABS),
    ("f(xy) = f(x)f(y)", "R", SIGN),
    ("f(xy) = f(x)f(y)", "Q", NONZERO),
    ("f(xy) = f(x)f(y)", "R", INVERSE),
    ("f(xy) = f(x)f(y)", "Q", INVERSE),
    ("f(x*f(y)) = y*f(x)", "R", INVERSE),
    ("f(x*f(y)) = y*f(x)", "Q", INVERSE),
    ("f(x)^2 = x^2", "R", ABS),
    ("f(x)^2 = x^2", "Q", ABS),
    ("f(x)^2 + y = x^2 + y", "R", ABS),
    ("f(f(x)) = x", "R", SWAP01),
    ("f(f(x)) = x", "Q", INVERSE),
    ("f(f(x)) + y = x + y", "R", SWAP01),
    ("f(f(x)) = f(x)", "R", POSITIVE_PART),
    ("f(f(x)) = f(x)", "Q", FLOOR),
    ("f(f(x)) = f(x)", "R", ABS),
    ("f(x^2) = x*f(x)", "R", UNIT),
    ("f(x^2) = f(x)^2", "R", ABS),
    ("f(x^2) = f(x)^2", "R", SIGN),
    ("f(-x) = f(x)", "R", ABS),
    ("f(x)f(y) = f(xy) + y - y", "Q", SIGN),
    ("f(x + y) = f(x) + f(y)", "R", CONJUGATION),
    ("f(x + y) = f(x) + f(y)", "R", RATIONAL_PART),
    ("f(x + f(y)) = f(x) + y", "R", CONJUGATION),                    # seed s37, which is stated over Q
    ("f(f(x) + y) = x + f(y)", "R", CONJUGATION),                    # s38
    ("f(f(x) + f(y)) = x + y", "R", CONJUGATION),                    # s39
    ("f(x - f(y)) = f(x) - y", "R", CONJUGATION),                    # s42
    ("f(x + y) + f(x - y) = 2f(x)", "R", CONJUGATION),               # s40
    ("f(x + y) + f(x - y) = 2f(x)", "R", RATIONAL_PART),
    ("f(x) + f(y) = 2f((x + y)/2)", "R", RATIONAL_PART),
    ("f(x + y) + f(x - y) = 2f(x) + 2f(y)", "R", NORM),              # s45 over R
    ("f(x + y) + f(x - y) = 2f(x) + 2f(y)", "R", SQUARE_OF_CONJUGATE),
    ("f(x + y) = f(x) + f(y) + 2xy - 2xy", "R", RATIONAL_PART),
    ("f(f(x)) = x", "R", CONJUGATION),
    ("f(x + y) - f(x) = f(y) - f(0)", "R", CONJUGATION),
]


def satisfies(problem: Problem, model: Model, rng: random.Random, points: int = 200) -> bool:
    """Does the model satisfy the equation at ``points`` random points?"""
    return all(value(problem.poly, model.fn, {name: model.point(rng) for name in "xyz"}) == 0 for _ in range(points))


def is_quadratic_on(model: Model, points: list) -> bool:
    """Does one polynomial of degree at most 2 pass through the model's values at all the (distinct) points?"""
    (x0, x1, x2), rest = points[:3], points[3:]
    f0, f1, f2 = (model.fn(x) for x in (x0, x1, x2))
    first = (f1 - f0) / (x1 - x0)
    second = ((f2 - f1) / (x2 - x1) - first) / (x2 - x0)
    return all(f0 + first * (x - x0) + second * (x - x0) * (x - x1) == model.fn(x) for x in rest)


def admits(branch, model: Model, rng: random.Random, samples: int = 4) -> bool:
    """Is the model in this case? Raises ``Unsound`` if the case claims something false about it."""
    fn = model.fn
    values: dict = {}
    for assumption in branch.assumptions:
        if assumption[0] == "witness":
            _, name, target = assumption
            if not model.surjective:
                raise Unsound(f"a preimage was named although f = {model.name} is not surjective")
            values[name] = model.preimage(value(target, fn, values))
        elif (assumption[0] == "zero") != (value(assumption[1], fn, values) == 0):
            return False
    for prop in ("injective", "surjective"):
        if prop in branch.props and not getattr(model, prop):
            raise Unsound(f"f is claimed {prop} but f = {model.name} is not")
    for _ in range(samples):
        point = dict(values)
        for name in "xyz":
            point[name] = model.point(rng)
        for row in branch.rows:
            if value(row, fn, point) != 0:
                raise Unsound(f"identity {row} = 0 fails for f = {model.name} at {point}")
        for known in branch.nonzero:
            if value(known, fn, point) == 0:
                raise Unsound(f"{known} is claimed nonzero but vanishes for f = {model.name}")
        s, t = point["x"], point["y"]
        claims = {"odd": fn(-s) == -fn(s), "even": fn(-s) == fn(s), "additive": fn(s + t) == fn(s) + fn(t),
                  "involution": fn(fn(s)) == s}
        for prop, holds in claims.items():
            if prop in branch.props and not holds:
                raise Unsound(f"f is claimed {prop} but f = {model.name} is not (at {s}, {t})")
    return True


def check_state(state, model: Model, rng: random.Random) -> None:
    """Raise ``Unsound`` if the state has lost the model or says something false about it."""
    if not any([admits(branch, model, rng) for branch in state.branches]):
        raise Unsound(f"f = {model.name} satisfies the equation but is in no open case"
                      + (": the problem was declared solved" if state.solved else ""))


def walk(problem: Problem, model: Model, rng: random.Random, steps: int, random_move) -> int:
    """Random moves from the start; every accepted state is checked. Returns the number of accepted moves.

    Half of the time the environment's own moves (free moves and routine
    substitutions) are applied as well, because that is how searches reach
    their states.
    """
    state = initial_state(problem)
    check_state(state, model, rng)
    accepted = 0
    for _ in range(steps):
        try:
            state = apply(state, random_move(rng, state))
        except Reject:
            continue
        accepted += 1
        check_state(state, model, rng)
        if rng.random() < 0.5:
            state, _ = close(state)
            check_state(state, model, rng)
    return accepted
