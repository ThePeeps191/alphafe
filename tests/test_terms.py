from fractions import Fraction

import pytest
from hypothesis import given, settings

from alphafe import terms as T
from alphafe.algebra import to_poly

from .strategies import terms


def test_parse_basic_shapes():
    assert T.parse("x") == T.Var("x")
    assert T.parse("a") == T.Sym("a")
    assert T.parse("12") == T.num(12)
    assert T.parse("f(x)") == T.App(T.Var("x"))
    assert T.parse("x + y") == T.Add(T.Var("x"), T.Var("y"))
    assert T.parse("x - y - z") == T.Sub(T.Sub(T.Var("x"), T.Var("y")), T.Var("z"))
    assert T.parse("-x^2") == T.Neg(T.Pow(T.Var("x"), 2))
    assert T.parse("3/4") == T.Num(Fraction(3, 4))


def test_implicit_multiplication():
    assert to_poly(T.parse("2x")) == to_poly(T.parse("2*x"))
    assert to_poly(T.parse("xf(y)")) == to_poly(T.parse("x*f(y)"))
    assert to_poly(T.parse("(x+y)(x-y)")) == to_poly(T.parse("x^2 - y^2"))
    assert to_poly(T.parse("2f(x)f(y)")) == to_poly(T.parse("2*f(x)*f(y)"))
    assert to_poly(T.parse("x/2")) == to_poly(T.parse("(1/2)*x"))


def test_precedence():
    assert to_poly(T.parse("x + y*z")) == to_poly(T.parse("x + (y*z)"))
    assert to_poly(T.parse("-x*y")) == to_poly(T.parse("-(x*y)"))
    assert to_poly(T.parse("x - -y")) == to_poly(T.parse("x + y"))
    assert to_poly(T.parse("2x^2")) == to_poly(T.parse("2*(x^2)"))


def test_parse_equation():
    lhs, rhs = T.parse_equation("f(x+f(y)) = f(x) + y")
    assert lhs == T.App(T.Add(T.Var("x"), T.App(T.Var("y"))))
    assert rhs == T.Add(T.App(T.Var("x")), T.Var("y"))


@pytest.mark.parametrize(
    "bad",
    ["", "x +", "f", "f x", "(x", "x)", "x / y", "x / 0", "x ^ y", "X", "x = y", "2 3", "x $ y", "1.5"],
)
def test_parse_rejects(bad):
    with pytest.raises(T.ParseError):
        T.parse(bad)


def test_equation_needs_one_equals():
    with pytest.raises(T.ParseError):
        T.parse_equation("x + y")
    with pytest.raises(T.ParseError):
        T.parse_equation("x = y = z")


def test_show_examples():
    assert T.show(T.parse("f(x+f(y))")) == "f(x + f(y))"
    assert T.show(T.parse("2*x*f(y)")) == "2xf(y)"
    assert T.show(T.parse("x*(y+1)")) == "x(y + 1)"
    assert T.show(T.parse("x/2")) == "x/2"
    assert T.show(T.parse("x*3")) == "x*3"


@given(terms)
@settings(max_examples=300, deadline=None)
def test_show_parse_round_trip(term):
    """Printing then parsing gives back an equal expression."""
    assert to_poly(T.parse(T.show(term))) == to_poly(term)


@given(terms)
@settings(max_examples=300, deadline=None)
def test_prefix_round_trip(term):
    """Prefix serialisation is lossless up to equality for small numbers."""
    assert to_poly(T.from_prefix(T.to_prefix(term))) == to_poly(term)


def test_prefix_examples():
    assert T.to_prefix(T.parse("f(x + f(y))")) == ["f", "+", "x", "f", "y"]
    assert T.to_prefix(T.Num(Fraction(-3, 2))) == ["~", "/", "3", "2"]
    assert T.from_prefix(["/", "3", "2"]) == T.Num(Fraction(3, 2))


@pytest.mark.parametrize("bad", [[], ["+", "x"], ["x", "y"], ["^", "x", "y"], ["/", "x", "2"], ["?"]])
def test_from_prefix_rejects(bad):
    with pytest.raises(T.ParseError):
        T.from_prefix(bad)


def test_structure_helpers():
    t = T.parse("f(f(x) + y) * a")
    assert T.nesting_depth(t) == 2
    assert T.term_vars(t) == {"x", "y"}
    assert T.term_syms(t) == {"a"}
    assert T.term_size(T.parse("x + y")) == 3
