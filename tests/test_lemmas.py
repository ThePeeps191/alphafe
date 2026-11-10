"""Standard lemmas over Q (polynomial Cauchy, the quadratic equation) and the unique-root deduction."""

import pytest

from alphafe.algebra import parse_poly
from alphafe.checker import Branch, Problem, cauchy_form, check
from alphafe.env import start
from alphafe.moves import parse_proof
from alphafe.solutions import parse_solution_set

P = parse_poly


def run(equation, domain, proof_text):
    return check(Problem.parse(equation, domain), parse_proof(proof_text))


# --- polynomial Cauchy ------------------------------------------------------

def test_cauchy_form_recognises_polynomial_defects():
    # plain Cauchy: p = 0, constant 0
    assert cauchy_form(P("f(x + y) - f(x) - f(y)")) == (P("0"), P("0"))
    # f(x+y) = f(x) + f(y) - f(0): constant -f(0)
    assert cauchy_form(P("f(x + y) - f(x) - f(y) + f(0)")) == (P("0"), P("-f(0)"))
    # f(x+y) = f(x) + f(y) + 2xy: f - x^2 is additive
    assert cauchy_form(P("f(x + y) - f(x) - f(y) - 2xy")) == (P("x^2"), P("0"))
    # f(x+y) = f(x) + f(y) + x^2 y + x y^2: f - x^3/3 is additive
    assert cauchy_form(P("f(x + y) - f(x) - f(y) - x^2*y - x*y^2")) == (P("x^3/3"), P("0"))
    # constant and polynomial together
    assert cauchy_form(P("2f(x + y) - 2f(x) - 2f(y) - 2xy - 6")) == (P("x^2/2"), P("3"))


def test_cauchy_form_rejects_impossible_defects():
    assert cauchy_form(P("f(x + y) - f(x) - f(y) - x^2*y")) is None        # not symmetric: not a coboundary
    assert cauchy_form(P("f(x + y) - f(x) - f(y) - x")) is None
    assert cauchy_form(P("f(x + y) - f(x) - 2f(y)")) is None
    assert cauchy_form(P("f(x + y) - f(x) - f(y) - f(x)f(y)")) is None      # the defect involves f
    assert cauchy_form(P("f(x + y) - f(x) - f(y) - y*f(0)")) is None


def test_polynomial_cauchy_solves_over_Q():
    result = run("f(x+y) = f(x) + f(y) + 2xy", "Q", "cauchy\nconclude")
    assert result.solved and result.solutions == parse_solution_set(["f(x) = x^2 + c*x"])
    result = run("f(x+y) = f(x) + f(y) + xy(x+y) + 1", "Q", "cauchy\nconclude")
    assert result.solved and result.solutions == parse_solution_set(["f(x) = x^3/3 + c*x - 1"])


def test_polynomial_cauchy_is_refused_over_R():
    result = run("f(x+y) = f(x) + f(y) + 2xy", "R", "cauchy")
    assert not result.ok and "over R" in result.error


# --- the quadratic functional equation ---------------------------------------

QUADRATIC = "f(x+y) + f(x-y) = 2f(x) + 2f(y)"


def test_quadratic_equation_over_Q():
    result = run(QUADRATIC, "Q", "quadratic\nconclude")
    assert result.solved and result.solutions == parse_solution_set(["f(x) = c*x^2"])


def test_quadratic_lemma_is_refused_over_R_and_on_other_shapes():
    assert "over R" in run(QUADRATIC, "R", "quadratic").error
    assert not run("f(x+y) + f(x-y) = 2f(x)", "Q", "quadratic").ok            # Jensen, not quadratic
    assert not run("f(x+y) + f(x-y) = 2f(x) + 2f(y) + 1", "Q", "quadratic").ok


def test_quadratic_and_polynomial_cauchy_are_free_moves():
    for equation, answer in [(QUADRATIC, "f(x) = c*x^2"), ("f(x+y) = f(x) + f(y) + 2xy", "f(x) = x^2 + c*x")]:
        state, proof = start(Problem.parse(equation, "Q"))
        assert state.solved and state.solution_set == parse_solution_set([answer])


# --- unique roots -------------------------------------------------------------

def test_unique_root_is_deduced():
    """t^2 = 0 leaves no choice (unlike t^2 = t), so f(x)^2 = 0 gives f(x) = 0 for every x."""
    branch = Branch("R")
    branch.add([P("f(x)^2")])
    assert P("f(x)") in branch.rows
    branch = Branch("R")
    branch.add([P("f(0)^3 - 1")])                      # (t - 1)(t^2 + t + 1): the quadratic has no real root
    assert P("f(0) - 1") in branch.rows


def test_unique_root_needs_certainty_about_other_roots():
    q = Branch("Q")
    q.add([P("f(0)^3 - 2f(0)^2 + f(0) - 2")])          # (t - 2)(t^2 + 1)
    assert P("f(0) - 2") in q.rows
    r = Branch("R")
    r.add([P("f(0)^3 - 2f(0)")])                       # t(t^2 - 2): over R also +-sqrt(2)
    assert P("f(0)") not in r.rows
    q = Branch("Q")
    q.add([P("f(0)^3 - 2f(0)")])                       # over Q only t = 0
    assert P("f(0)") in q.rows


def test_two_roots_are_never_merged():
    """The pointwise trap again: f(x)^2 = f(x) must stay a quadratic relation."""
    branch = Branch("R")
    branch.add([P("f(x)^2 - f(x)")])
    assert set(branch.rows) == {P("f(x)^2 - f(x)"), P("f(y)^2 - f(y)")}   # (one copy per variable name)
