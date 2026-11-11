"""No sequence of accepted moves may lose a solution that is not a polynomial (see tests/nonpoly.py)."""

import random
import zlib
from fractions import Fraction

import pytest

from alphafe.baseline.search import brute_force
from alphafe.checker import Problem, Reject, apply, initial_state
from alphafe.modelcheck import Unsound
from alphafe.moves import parse_move

from .nonpoly import ABS, CASES, CONJUGATION, S2, check_state, is_quadratic_on, satisfies, value, walk
from .test_modelcheck import random_move

IDS = [f"{equation} [{domain}] {model.name}" for equation, domain, model in CASES]


def test_sqrt2_arithmetic_is_exact():
    root = S2(0, 1)
    assert root * root == 2 and (1 + root) * (1 - root) == -1 and (1 + root) ** 3 == S2(7, 5)
    assert S2(3) == Fraction(3) and Fraction(3) == S2(3) and S2(1, 1) != 1
    assert S2(7, 5) / S2(1, 1) == S2(3, 2) and 1 / root * root == 1
    assert CONJUGATION.fn(S2(2, 3)) == S2(2, -3) and CONJUGATION.fn(Fraction(5)) == 5


@pytest.mark.parametrize("equation, domain, model", CASES, ids=IDS)
def test_the_model_solves_its_equation_and_is_not_a_polynomial_there(equation, domain, model):
    problem = Problem.parse(equation, domain)
    rng = random.Random(zlib.crc32(equation.encode()))
    assert satisfies(problem, model, rng)
    # Not c2*x^2 + c1*x + c0: some six of its own test points lie on no such curve.
    for _ in range(40):
        points = []
        while len(points) < 6:
            candidate = model.point(rng)
            if all(candidate != other for other in points):
                points.append(candidate)
        if not is_quadratic_on(model, points):
            return
    pytest.fail(f"{model.name} looks like a polynomial of degree at most 2 on its test points")


@pytest.mark.parametrize("equation, domain, model", CASES, ids=IDS)
def test_random_walks_never_lose_a_non_polynomial_solution(equation, domain, model):
    problem = Problem.parse(equation, domain)
    rng = random.Random(zlib.crc32(f"{equation}{domain}{model.name}".encode()))
    for _ in range(12):
        walk(problem, model, rng, 40, random_move)


@pytest.mark.parametrize("equation, domain", sorted({(equation, domain) for equation, domain, _ in CASES}))
def test_search_never_solves_a_problem_that_has_a_non_polynomial_solution(equation, domain):
    result = brute_force(Problem.parse(equation, domain), max_calls=250, max_seconds=30)
    assert not result.solved, f"claimed {result.solutions}"


def test_the_check_itself_catches_an_unsound_step():
    """A positive control: the same conjugation against Cauchy's equation over Q, where the lemma is allowed.

    Over Q every additive function is linear, and the checker says so. The
    model is not linear on Q(sqrt 2), so the check must object; if it did
    not, the walks above would be vacuous.
    """
    state = initial_state(Problem.parse("f(x + y) = f(x) + f(y)", "Q"))
    state = apply(state, parse_move("cauchy"))
    with pytest.raises(Unsound):
        check_state(state, CONJUGATION, random.Random(0))


def test_cancelling_needs_real_injectivity_even_for_constants():
    """f(a) = f(b) gives a = b only for an injective f; |x| has f(1) = f(-1)."""
    problem = Problem.parse("f(x)^2 = x^2", "R")
    state = initial_state(problem)
    for text in ("sub P: x:=1", "sub P: x:=-1"):
        state = apply(state, parse_move(text))
    with pytest.raises(Reject):
        apply(state, parse_move("cancel"))
    check_state(state, ABS, random.Random(1))
    assert value(problem.poly, ABS.fn, {"x": Fraction(-3), "y": Fraction(0), "z": Fraction(0)}) == 0
