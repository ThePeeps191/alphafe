"""Answer guesser: try polynomial templates and solve for the coefficients.

This finds candidate *answers*, not proofs: it tells us which polynomials of
degree at most 2 satisfy the equation, but says nothing about other
functions. It is useful as a sanity check and as a cheap baseline.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .. import terms as T
from ..algebra import Unsupported, parse_poly
from ..checker import Problem
from ..solutions import SolutionSet, fit_candidate, make_solution_set

# Substituting a quadratic into an equation with an exponent n gives a polynomial of degree 2n. Its
# expansion takes seconds at n = 50 and does not finish at n = 2000, so above this no template is tried.
MAX_EXPONENT = 40

TEMPLATES = (
    ("quadratic", "a*x^2 + b*x + c"),
    ("linear", "a*x + b"),
    ("constant", "c"),
)


@dataclass
class Guess:
    solutions: Optional[SolutionSet]   # None if no template could be solved exactly
    template: str = ""                 # the richest template that was solved
    skipped: tuple = ()                # richer templates whose coefficient system could not be solved exactly
    exponent: int = 0                  # set when nothing was tried because the equation's exponent is too large

    def __str__(self) -> str:
        if self.exponent:
            return f"no guess (an exponent of {self.exponent} is too large to try polynomials)"
        if self.solutions is None:
            return "no guess"
        return f"{self.solutions} (among {self.template} functions)"


def equation_exponent(equation: str) -> int:
    """The largest exponent written in an equation (nested powers multiplied)."""
    return max(T.max_exponent(side) for side in T.parse_equation(equation))


def guess(problem: Problem) -> Guess:
    """All solutions among the richest template whose coefficient system we can solve exactly.

    The quadratic template contains the linear and constant ones, so it is
    tried first; the smaller templates are fallbacks for when its coefficient
    system is too hard for the exact solver.
    """
    exponent = equation_exponent(problem.equation)
    if exponent > MAX_EXPONENT:
        return Guess(None, exponent=exponent)
    skipped = []
    for name, text in TEMPLATES:
        try:
            fits = fit_candidate(problem.poly, parse_poly(text), problem.domain)
        except Unsupported:
            skipped.append(name)
            continue
        return Guess(make_solution_set(fits), name, tuple(skipped))
    return Guess(None, "", tuple(skipped))
