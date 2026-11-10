"""The checker accepts correct proofs and computes the right solution sets."""

import pytest

from alphafe.algebra import equation_poly, parse_poly
from alphafe.checker import (
    Branch, Problem, Reject, apply, cauchy_constant, check, detect_property, explicit_form,
    initial_state, injectivity_variable, surjectivity_variable, verify_solution,
)
from alphafe.moves import parse_move, parse_proof
from alphafe.solutions import parse_solution_set

from .seedlib import expected, load_seeds, seed_problem, seed_proofs

P = parse_poly
E = equation_poly


def run(equation, domain, proof_text):
    return check(Problem.parse(equation, domain), parse_proof(proof_text))


def rows_of(state):
    return set(state.current.rows)


# --- the seed benchmark -----------------------------------------------------

def test_seed_file_is_well_formed():
    seeds = load_seeds()
    assert len(seeds) >= 40
    assert len({s["id"] for s in seeds}) == len(seeds)
    for s in seeds:
        assert s["domain"] in ("R", "Q") and s["source"] == "seed" and s["mohs"] % 5 == 0
        problem = seed_problem(s)
        assert 2 <= len(problem.poly.variables()) <= 3
        for solution in s["solutions"]:
            assert verify_solution(problem, solution), (s["id"], solution)


def test_at_least_fifteen_hand_proofs():
    assert len(seed_proofs()) >= 15


@pytest.mark.parametrize("record, proof", seed_proofs(), ids=lambda v: v["id"] if isinstance(v, dict) else "")
def test_hand_written_proof_checks(record, proof):
    result = check(seed_problem(record), proof)
    assert result.ok, result.error
    assert result.solved, result.error
    assert result.solutions == expected(record)


# --- problems ---------------------------------------------------------------

@pytest.mark.parametrize(
    "equation, domain",
    [("f(x) = a", "R"), ("x + y = y + x", "R"), ("f(x+y) = f(x)", "Z"), ("f(x + y) = f(x + y)", "R"), ("x = y", "R")],
)
def test_bad_problems_are_refused(equation, domain):
    with pytest.raises(ValueError):
        Problem.parse(equation, domain)


# --- individual moves -------------------------------------------------------

def test_substitution_adds_the_instance():
    state = initial_state(Problem.parse("f(x+y) = f(x) + y"))
    state = apply(state, parse_move("sub P: x:=0"))
    assert P("f(y) - f(0) - y") in rows_of(state)
    # ... and the one-variable identity is also recorded for x
    assert P("f(x) - f(0) - x") in rows_of(state)


def test_useless_moves_are_rejected():
    state = initial_state(Problem.parse("f(x+y) = f(x) + y"))
    for text in ["sub P: x:=x", "sub P: y:=0", "sub P: z:=0", "sub R7: x:=0", "sub [f(x) = x]: x:=0"]:
        with pytest.raises(Reject):
            apply(state, parse_move(text))


def test_linear_elimination():
    """Two instances combine without an explicit move: 2f(x) + f(-x) = x and its mirror give f."""
    state = initial_state(Problem.parse("2f(x) + f(-x) + f(y) = x + f(y)"))
    state = apply(state, parse_move("sub P: x:=-x"))
    assert P("f(x) - x") in rows_of(state)


def test_ground_rule_rewrites_inside_f():
    state = initial_state(Problem.parse("f(x + f(0)) + y = f(x) + y + f(0)"))
    state = apply(state, parse_move("sub P: x:=0"))  # f(f(0)) = 2f(0)
    assert P("f(f(0)) - 2f(0)") in rows_of(state)


def test_coefficient_extraction():
    """An identity without f of a variable gives one fact per coefficient."""
    branch = Branch("R")
    branch.add([P("x*f(0) + y*f(1) - y")])
    assert set(branch.rows) == {P("f(0)"), P("f(1) - 1")}


def test_variable_cancellation_needs_the_value_at_zero():
    branch = Branch("R")
    branch.add([P("x*f(x) - x")])              # says nothing at x = 0
    assert P("f(x) - 1") not in branch.rows
    branch.add([P("f(0) - 1")])                # now Q(0) = f(0) - 1 = 0 is known
    branch.add([P("y*f(y) - y")])
    assert P("f(y) - 1") in branch.rows


def test_properties_are_detected_and_used():
    branch = Branch("R")
    branch.add([P("f(-x) + f(x)")])
    assert "odd" in branch.props
    assert branch.norm(P("f(-y - 1)")) == P("-f(y + 1)")
    assert branch.norm(P("f(0)")) == P("0")

    branch = Branch("R")
    branch.add([P("f(f(x)) - x")])
    assert {"involution", "injective", "surjective"} <= branch.props
    assert branch.norm(P("f(f(y + 1))")) == P("y + 1")

    branch = Branch("R")
    branch.add([P("f(x + y) - f(x) - f(y)")])
    assert "additive" in branch.props
    assert branch.norm(P("f(2x - 3y + 1)")) == P("2f(x) - 3f(y) + f(1)")

    branch = Branch("R")
    branch.add([P("f(-x) - f(x)")])
    assert "even" in branch.props
    assert branch.norm(P("f(-x)")) == P("f(x)")


def test_detect_property():
    assert detect_property(P("f(-y) + f(y)")) == "odd"
    assert detect_property(P("f(f(x)) - x")) == "involution"
    assert detect_property(P("f(x + y) - f(x) - f(y)")) == "additive"
    assert detect_property(P("f(x + y) - f(x) - f(y) - 1")) is None
    assert detect_property(P("f(f(x)) - 2x")) is None


def test_injectivity_criterion():
    b = Branch("R")
    assert injectivity_variable(b, E("f(f(y)) = y + f(0)")) == "y"
    assert injectivity_variable(b, E("f(x + f(y)) = f(x) + y")) == "y"
    assert injectivity_variable(b, E("f(f(x)) = x^2")) is None
    assert injectivity_variable(b, E("f(x + y) = f(x) + f(y)")) is None
    assert injectivity_variable(b, E("f(f(y)) = y*f(1)")) is None     # f(1) not known nonzero
    assert injectivity_variable(b, E("f(y + f(y)) = y")) is None      # y also occurs outside f(y)
    b.nonzero.append(P("f(1)"))
    assert injectivity_variable(b, E("f(f(y)) = y*f(1)")) == "y"


def test_surjectivity_criterion():
    b = Branch("R")
    assert surjectivity_variable(b, E("f(f(y)) = y + f(0)")) == "y"
    assert surjectivity_variable(b, E("f(x + f(y)) = f(x) + y")) == "y"
    assert surjectivity_variable(b, E("f(x + y) = f(x) + f(y)")) is None
    assert surjectivity_variable(b, E("f(x)f(y) = x")) is None        # a product, not a single f
    assert surjectivity_variable(b, E("f(f(y)) = y^2")) is None


def test_explicit_form():
    x = P("x")
    assert explicit_form(P("f(y) - y - f(0)")) == P("x + f(0)")
    assert explicit_form(P("2f(x) - x")) == P("x/2")
    assert explicit_form(P("f(2x + 1) - x")) == P("(x - 1)/2")
    assert explicit_form(P("f(x - a) - x + 2a")) == P("x - a")
    assert explicit_form(P("x*f(x) - x^2")) is None       # says nothing at x = 0
    assert explicit_form(P("f(x)^2 - x^2")) is None       # pointwise sign choice
    assert explicit_form(P("f(x) - f(y) - x + y")) is None
    assert explicit_form(P("f(x) + f(-x)")) is None
    assert explicit_form(P("f(x^2) - x^2")) is None       # only determines f on squares
    assert explicit_form(P("f(x) - x*f(x + 1)")) is None


def test_cauchy_constant():
    assert cauchy_constant(P("f(x + y) - f(x) - f(y)")) == P("0")
    assert cauchy_constant(P("2f(x + y) - 2f(x) - 2f(y) + 2f(0)")) == P("f(0)")
    assert cauchy_constant(P("f(x + y) - f(x) - f(y) - x")) is None
    assert cauchy_constant(P("f(x + y) - f(x) - 2f(y)")) is None


def test_case_split_and_branch_locality():
    result = run("f(x)f(y) = f(x+y) + xy", "R", """
        sub P: x:=0, y:=0
        split [f(0)^2 = f(0)]
        sub P: y:=0
    """)
    assert result.ok and not result.solved
    state = result.state
    assert len(state.branches) == 2 and P("f(x)") in rows_of(state)
    # close the first case; the fact f(x) = 0 must not leak into the second
    state = apply(state, parse_move("conclude"))
    assert len(state.branches) == 1
    assert P("f(x)") not in rows_of(state) and P("f(0) - 1") in rows_of(state)
    with pytest.raises(Reject):
        apply(state, parse_move("conclude"))


def test_contradiction_closes_a_case():
    result = run("f(x)f(y) = f(xy) + x + y", "R", """
        sub P: x:=0, y:=0
        split [f(0)^2 = f(0)]
        sub P: y:=0
    """)
    assert result.ok
    assert len(result.state.branches) == 1                 # the case f(0) = 0 died: 0 = x
    assert result.state.log[-1].closed == "contradiction"


def test_splitnz_and_automatic_division():
    result = run("f(x)f(y) = f(x)", "R", """
        splitnz f(0)
        sub P: y:=0        # case f(0) = 0: f(x)*0 = f(x)
        conclude
        sub P: x:=0        # case f(0) != 0: f(0)f(y) = f(0), divide by f(0)
        conclude
    """)
    assert result.solved and result.solutions == parse_solution_set(["f(x) = 0", "f(x) = 1"])


def test_no_roots_contradiction_depends_on_domain():
    over_q = run("f(x)^2 + y = 2 + y + f(x) - f(x)", "Q", "")
    assert over_q.solved and len(over_q.solutions) == 0   # f(x)^2 = 2 has no rational solution
    over_r = run("f(x)^2 + y = 2 + y + f(x) - f(x)", "R", "")
    assert not over_r.solved                               # over R it has (pointwise!) solutions


def test_incomplete_proof_is_not_solved():
    result = run("f(x+y) = f(x) + y", "R", "sub P: x:=0")
    assert result.ok and not result.solved and result.solutions is None


def test_rejected_move_reports_position_and_reason():
    result = run("f(x+y) = f(x) + y", "R", "sub P: x:=0\ncancel\nconclude")
    assert not result.ok and result.step == 1 and "injectivity" in result.error


def test_moves_after_completion_are_rejected():
    result = run("f(x+y) = f(x) + y", "R", "sub P: x:=0\nconclude\nconclude")
    assert not result.ok and result.step == 2


def test_conclude_reports_family_members_only():
    """f(x) = x + f(0) is concluded, then f(0) is pinned down by substituting back."""
    result = run("f(x+y) + f(x) = 2x + y", "R", "sub P: x:=0\nconclude")
    assert result.solved and str(result.solutions) == "f(x) = x"
