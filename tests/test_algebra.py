from fractions import Fraction

import pytest
import sympy
from hypothesis import given, settings
from hypothesis import strategies as st

from alphafe import terms as T
from alphafe.algebra import (
    Poly,
    ZERO,
    Unsupported,
    apply_function,
    div_exact,
    equation_poly,
    equation_str,
    evaluate,
    factor_hint,
    has_no_root,
    leading_mono,
    monic,
    parse_poly,
    poly_str,
    poly_term,
    rational_roots,
    split_by_vars,
    to_poly,
)

from .strategies import small_fracs, terms

P = parse_poly


# --- canonical form ---------------------------------------------------------

def test_equal_expressions_have_equal_polys():
    assert P("(x+y)^2") == P("x^2 + 2xy + y^2")
    assert P("f(x+y)") == P("f(y+x)")
    assert P("f(2x - x)") == P("f(x)")
    assert P("f(x)f(y)") == P("f(y)f(x)")
    assert P("x - x") == ZERO
    assert P("f((x+1)^2)") == P("f(x^2 + 2x + 1)")


def test_different_expressions_differ():
    assert P("f(x+y)") != P("f(x) + f(y)")
    assert P("f(x)") != P("f(y)")
    assert P("f(f(x))") != P("f(x)")
    assert P("a") != P("x")


def test_hash_and_key_agree_with_equality():
    a, b = P("x*f(y) + 1"), P("1 + f(y)*x")
    assert a == b and hash(a) == hash(b) and a.key == b.key


@given(terms, terms, terms)
@settings(max_examples=150, deadline=None)
def test_ring_axioms(a, b, c):
    pa, pb, pc = to_poly(a), to_poly(b), to_poly(c)
    assert pa + pb == pb + pa
    assert pa * pb == pb * pa
    assert (pa + pb) + pc == pa + (pb + pc)
    assert (pa * pb) * pc == pa * (pb * pc)
    assert pa * (pb + pc) == pa * pb + pa * pc
    assert pa - pa == ZERO
    assert pa + ZERO == pa
    assert pa * Poly.const(1) == pa
    assert -(-pa) == pa


@given(terms)
@settings(max_examples=200, deadline=None)
def test_no_zero_coefficients_stored(term):
    poly = to_poly(term)
    assert all(c != 0 for c in poly.terms.values())
    assert all(isinstance(c, Fraction) for c in poly.terms.values())


# --- SymPy cross-check ------------------------------------------------------

_F = sympy.Function("f")


def to_sympy(term):
    if isinstance(term, T.Num):
        return sympy.Rational(term.value.numerator, term.value.denominator)
    if isinstance(term, (T.Var, T.Sym)):
        return sympy.Symbol(term.name)
    if isinstance(term, T.App):
        return _F(sympy.expand(to_sympy(term.arg)))
    if isinstance(term, T.Add):
        return to_sympy(term.left) + to_sympy(term.right)
    if isinstance(term, T.Sub):
        return to_sympy(term.left) - to_sympy(term.right)
    if isinstance(term, T.Mul):
        return to_sympy(term.left) * to_sympy(term.right)
    if isinstance(term, T.Neg):
        return -to_sympy(term.arg)
    if isinstance(term, T.Pow):
        return to_sympy(term.base) ** term.exp
    raise TypeError(term)


@given(terms)
@settings(max_examples=150, deadline=None)
def test_canonical_form_matches_sympy(term):
    """Our canonical polynomial, printed back, expands to the same thing in SymPy."""
    ours = to_sympy(poly_term(to_poly(term)))
    theirs = to_sympy(term)
    assert sympy.expand(ours - theirs) == 0


@given(terms, terms)
@settings(max_examples=150, deadline=None)
def test_equality_matches_sympy(a, b):
    ours = to_poly(a) == to_poly(b)
    theirs = sympy.expand(to_sympy(a) - to_sympy(b)) == 0
    assert ours == theirs


# --- substitution and rewriting --------------------------------------------

def test_subst_reaches_inside_f():
    p = P("f(x + y) - f(x) - y")
    assert p.subst({"x": P("0")}) == P("f(y) - f(0) - y")
    assert p.subst({"x": P("f(y)")}) == P("f(f(y) + y) - f(f(y)) - y")


def test_subst_is_simultaneous():
    p = P("f(x) + 2y")
    assert p.subst({"x": P("y"), "y": P("x")}) == P("f(y) + 2x")


@given(terms, terms, small_fracs, small_fracs, small_fracs)
@settings(max_examples=150, deadline=None)
def test_subst_commutes_with_evaluation(a, b, vx, vy, vz):
    """Evaluating a[x := b] equals evaluating a with x set to the value of b."""
    func = lambda t: 2 * t * t - 3 * t + 1
    env = {"x": vx, "y": vy, "z": vz, "a": Fraction(2), "b": Fraction(-1)}
    pa, pb = to_poly(a), to_poly(b)
    direct = evaluate(pa.subst({"x": pb}), func, env)
    env2 = dict(env, x=evaluate(pb, func, env))
    assert direct == evaluate(pa, func, env2)


@given(terms, terms, small_fracs, small_fracs)
@settings(max_examples=150, deadline=None)
def test_arithmetic_commutes_with_evaluation(a, b, vx, vy):
    func = lambda t: 3 * t - 2
    env = {"x": vx, "y": vy, "z": Fraction(1, 2), "a": Fraction(2), "b": Fraction(-1)}
    pa, pb = to_poly(a), to_poly(b)
    ea, eb = evaluate(pa, func, env), evaluate(pb, func, env)
    assert evaluate(pa + pb, func, env) == ea + eb
    assert evaluate(pa * pb, func, env) == ea * eb
    assert evaluate(pa - pb, func, env) == ea - eb


def test_replace_atoms_is_deep():
    p = P("f(f(0) + x) + f(0)^2")
    f0 = next(iter(P("f(0)").top_atoms()))
    assert p.replace_atoms({f0: P("1")}) == P("f(1 + x) + 1")


def test_rewrite_returns_same_object_when_unchanged():
    p = P("f(x) + y")
    assert p.rewrite(lambda atom: None) is p
    assert p.subst({"z": P("1")}) is p


def test_variables_and_atoms():
    p = P("f(x + f(y)) + a")
    assert p.variables() == {"x", "y"}
    assert P("f(0) + a").is_ground()
    assert p.contains_atom(("v", "y"))
    assert not p.contains_atom(("v", "z"))
    assert len(p.all_atoms()) == 5  # f(x+f(y)), x, f(y), y, a


def test_apply_function():
    eq = equation_poly("f(x + f(y)) = f(x) + y")
    assert apply_function(eq, P("x")).is_zero()
    assert apply_function(eq, P("-x")).is_zero()
    assert not apply_function(eq, P("2x")).is_zero()
    # parametrised: f(x) = c x leaves (c^2 - 1) y
    assert apply_function(eq, P("c*x")) == P("c^2*y - y")


# --- ranking, division, roots ----------------------------------------------

def test_leading_monomial_is_most_nested():
    assert Poly({leading_mono(P("f(x+y) - f(x) - y")): 1}) == P("f(x+y)")
    assert Poly({leading_mono(P("f(f(x)) - x - f(0)")): 1}) == P("f(f(x))")
    assert Poly({leading_mono(P("f(x) - x*f(f(0))")): 1}) == P("f(x)")
    assert Poly({leading_mono(P("f(x) + f(-x)")): 1}) == P("f(-x)")


def test_monic():
    assert monic(P("2f(x) - 4x")) == P("f(x) - 2x")
    assert monic(ZERO) == ZERO


def test_split_by_vars():
    parts = split_by_vars(P("x*f(0) + x*a - 3y^2 + f(1)"))
    assert parts[(((("v", "x")), 1),)] == P("f(0) + a")
    assert parts[()] == P("f(1)")
    assert len(parts) == 3


@given(terms, terms)
@settings(max_examples=150, deadline=None)
def test_div_exact_inverts_multiplication(a, b):
    pa, pb = to_poly(a), to_poly(b)
    if pb.is_zero():
        return
    assert div_exact(pa * pb, pb) == pa


def test_div_exact_detects_non_divisibility():
    assert div_exact(P("x^2 + 1"), P("x + 1")) is None
    assert div_exact(P("f(0)*x + 1"), P("f(0)")) is None
    assert div_exact(P("x^2 - 1"), P("x + 1")) == P("x - 1")
    with pytest.raises(ZeroDivisionError):
        div_exact(P("x"), ZERO)


def test_rational_roots():
    F = Fraction
    assert rational_roots([F(-1), F(0), F(1)]) == [F(-1), F(1)]
    assert rational_roots([F(0), F(-1), F(1)]) == [F(0), F(1)]
    assert rational_roots([F(-2), F(0), F(1)]) == []
    assert rational_roots([F(1), F(-3), F(2)]) == [F(1, 2), F(1)]
    assert rational_roots([F(0), F(0), F(1)]) == [F(0)]
    assert rational_roots([F(5)]) == []
    with pytest.raises(Unsupported):
        rational_roots([F(10**8 + 7), F(1), F(10**8 + 9)])


@given(st.lists(small_fracs, min_size=1, max_size=3), small_fracs)
@settings(max_examples=150, deadline=None)
def test_rational_roots_finds_planted_roots(roots, lead):
    if lead == 0:
        return
    coeffs = [Fraction(lead)]
    for r in roots:  # multiply by (t - r)
        coeffs = [Fraction(0)] + coeffs
        for i in range(len(coeffs) - 1):
            coeffs[i] -= r * coeffs[i + 1]
    found = rational_roots(coeffs)
    assert set(roots) <= set(found)
    for r in found:
        assert sum(c * r**i for i, c in enumerate(coeffs)) == 0


def test_has_no_root_depends_on_domain():
    F = Fraction
    x2_minus_2 = [F(-2), F(0), F(1)]
    assert has_no_root(x2_minus_2, "Q")          # sqrt(2) is irrational
    assert not has_no_root(x2_minus_2, "R")      # ... but it is real
    assert has_no_root([F(1), F(0), F(1)], "R")  # x^2 + 1
    assert has_no_root([F(1), F(1), F(1)], "R")  # x^2 + x + 1
    assert has_no_root([F(1), F(0), F(0), F(0), F(1)], "R")  # x^4 + 1
    assert not has_no_root([F(-1), F(0), F(1)], "Q")
    assert not has_no_root([F(2), F(0), F(0), F(1)], "R")  # cubic: a real root exists
    assert has_no_root([F(3)], "R")


def _product(factors):
    out = Poly.const(1)
    for factor, mult in factors:
        out = out * factor**mult
    return out


@pytest.mark.parametrize(
    "text, n_factors",
    [
        ("f(0)^2 - f(0)", 2),
        ("f(1)*f(-1)", 2),
        ("f(0)^2", 1),
        ("f(0)^3 - f(0)", 3),
        ("a*b - 2a - b + 2", 2),
        ("f(0)^2 - 2", 1),
        ("f(0)^2*f(1) - f(1)", 3),
    ],
)
def test_factor_hint(text, n_factors):
    poly = P(text)
    factors = factor_hint(poly)
    assert len(factors) == n_factors
    ratio = div_exact(poly, _product(factors))
    assert ratio is not None and ratio.const_value() not in (None, 0)


# --- printing ---------------------------------------------------------------

def test_printing():
    assert poly_str(P("f(x+y) - f(x) - y")) == "f(x + y) - f(x) - y"
    assert equation_str(P("f(x+y) - f(x) - y")) == "f(x + y) = f(x) + y"
    assert equation_str(P("f(0)^2 - f(0)")) == "f(0)^2 = f(0)"
    assert equation_str(P("2f(x) - x")) == "2f(x) = x"
    assert poly_str(ZERO) == "0"


@given(terms)
@settings(max_examples=200, deadline=None)
def test_print_parse_round_trip(term):
    poly = to_poly(term)
    assert parse_poly(poly_str(poly)) == poly
