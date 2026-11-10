from fractions import Fraction

import pytest

from alphafe.algebra import Poly, Unsupported, equation_poly, parse_poly
from alphafe.solutions import (
    fit_candidate, make_family, make_solution_set, parse_solution, parse_solution_set,
    solve_system, verify,
)
from alphafe.terms import ParseError

P = parse_poly
a, b, c = ("c", "a"), ("c", "b"), ("c", "c")


def points(solutions):
    return sorted(tuple(sorted((k[1], str(v)) for k, v in s.items())) for s in solutions)


def test_solve_linear():
    assert points(solve_system([P("2a - 4")], "R")) == [(("a", "2"),)]
    assert points(solve_system([P("a + b - 1"), P("a - b")], "R")) == [(("a", "1/2"), ("b", "1/2"))]


def test_solve_keeps_free_parameters():
    (sol,) = solve_system([P("a - b")], "R")
    assert len(sol) == 1  # one parameter expressed through the other, which stays free


def test_solve_univariate_roots():
    assert points(solve_system([P("a^2 - 1")], "R")) == [(("a", "-1"),), (("a", "1"),)]
    assert points(solve_system([P("a^2 - a")], "Q")) == [(("a", "0"),), (("a", "1"),)]
    assert solve_system([P("a^2 + 1")], "R") == []
    assert solve_system([P("a^2 - 2")], "Q") == []


def test_solve_refuses_irrational_answers_over_R():
    with pytest.raises(Unsupported):
        solve_system([P("a^2 - 2")], "R")


def test_solve_common_factor_branches():
    sols = points(solve_system([P("a*b - a")], "R"))
    assert sols == [(("a", "0"),), (("b", "1"),)]


def test_solve_inconsistent():
    assert solve_system([P("a - 1"), P("a - 2")], "R") == []
    assert solve_system([Poly.const(1)], "R") == []
    assert solve_system([], "R") == [{}]


def test_solve_refuses_what_it_cannot_do():
    with pytest.raises(Unsupported):
        solve_system([P("a*b - 1")], "R")


def test_solutions_satisfy_the_system():
    eqs = [P("a^2 - b"), P("b - 1"), P("c*a - c")]
    for sol in solve_system(eqs, "R"):
        for eq in eqs:
            assert eq.replace_atoms(sol).is_zero()
    # exactly two components: a = 1 with c free, and a = -1 with c = 0
    assert points(solve_system(eqs, "R")) == [
        (("a", "-1"), ("b", "1"), ("c", "0")),
        (("a", "1"), ("b", "1")),
    ]


def test_verify():
    eq = equation_poly("f(x + f(y)) = f(x) + y")
    assert verify(eq, P("x")) and verify(eq, P("-x"))
    assert not verify(eq, P("x + 1"))
    eq2 = equation_poly("f(x+y) = f(x) + y")
    assert verify(eq2, P("x + c"))          # for every c at once
    assert not verify(eq2, P("c*x"))        # not for every c
    with pytest.raises(ValueError):
        verify(eq2, P("f(x)"))
    with pytest.raises(ValueError):
        verify(eq2, P("y"))


def test_fit_candidate():
    eq = equation_poly("f(x + f(y)) = f(x) + y")
    fits = make_solution_set(fit_candidate(eq, P("a*x + b"), "Q"))
    assert fits == parse_solution_set(["f(x) = x", "f(x) = -x"])
    eq2 = equation_poly("f(x+y) = f(x) + y")
    assert make_solution_set(fit_candidate(eq2, P("a*x^2 + b*x + c"), "R")) == parse_solution_set(["f(x) = x + c"])


def test_family_canonical_forms_agree():
    assert make_family(P("c*x")) == make_family(P("2a*x"))
    assert make_family(P("c*x + d")) == make_family(P("(a + b)*x + a - b"))
    assert make_family(P("x + c")) == make_family(P("x + 1 - 3c"))
    assert make_family(P("c*x")) != make_family(P("c*x + 1"))
    assert make_family(P("x + c - c")) == make_family(P("x"))
    assert str(make_family(P("a*x + b"))) == "f(x) = cx + d"


def test_family_with_a_free_coefficient_is_recognised():
    assert make_family(P("x^2 - a^2 + b")) == make_family(P("x^2 + c"))
    assert make_family(P("x + a - 2b")) == make_family(P("x + c"))
    assert make_family(P("(a^2 + b)*x + a^3 + c")) == make_family(P("c*x + d"))
    # genuinely non-affine families keep their shape but still answer membership questions
    curve = make_family(P("c*x + c^2"))
    assert curve.affine is None
    assert curve.contains(make_family(P("2x + 4"))) and not curve.contains(make_family(P("2x + 5")))


def test_family_containment():
    line = make_family(P("c*x + d"))
    assert line.contains(make_family(P("x")))
    assert line.contains(make_family(P("c*x")))
    assert not make_family(P("c*x")).contains(make_family(P("x + 1")))
    assert not make_family(P("x")).contains(line)


def test_solution_set_is_order_and_redundancy_independent():
    s1 = parse_solution_set(["f(x) = x", "f(x) = -x"])
    s2 = parse_solution_set(["f(x) = -x", "f(x) = x", "f(x) = x"])
    assert s1 == s2
    assert parse_solution_set(["f(x) = 0", "f(x) = c*x"]) == parse_solution_set(["f(x) = a*x"])
    assert parse_solution_set([]) != s1
    assert str(parse_solution_set([])) == "no solutions"
    assert s1.contains_function(P("x")) and not s1.contains_function(P("2x"))


def test_parse_solution_rejects():
    for bad in ["x", "f(y) = y", "f(x) = y", "f(x) = f(x)"]:
        with pytest.raises(ParseError):
            parse_solution(bad)
