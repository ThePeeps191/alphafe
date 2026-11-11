"""Deliberately wrong proofs. Each one makes a classic mistake; the checker must refuse it.

Every test names the trap, shows the bogus step being rejected, and (where it
makes sense) shows that the wrong answer the mistake leads to is indeed wrong.
"""

import pytest

from alphafe.checker import Problem, Reject, apply, check, initial_state, verify_solution
from alphafe.moves import Subst, parse_move, parse_proof
from alphafe.terms import ParseError, parse
from alphafe.solutions import parse_solution_set


def run(equation, domain, proof_text):
    return check(Problem.parse(equation, domain), parse_proof(proof_text))


def rejected(result, *words):
    assert not result.ok, "the wrong proof was accepted"
    for word in words:
        assert word in result.error, result.error
    return True


# --- Trap 1: the pointwise trap --------------------------------------------

POINTWISE = "f(x)^2 + y = x*f(x) + y"   # i.e. f(x)(f(x) - x) = 0 for every x


def test_pointwise_trap_split_on_identity_with_variables():
    """From "f(x) = 0 or f(x) = x for each x" one may not split into f = 0 / f = x:
    f(x) = x for x > 0 and 0 otherwise also satisfies the identity."""
    assert rejected(run(POINTWISE, "R", "split R1"), "pointwise")
    assert rejected(run(POINTWISE, "R", "split P"), "pointwise")
    assert rejected(run(POINTWISE, "R", "split [f(x)^2 = x*f(x)]"), "pointwise")
    assert rejected(run(POINTWISE, "R", "split P by f(x), f(x) - x"))


def test_pointwise_trap_no_conclusion_from_a_product():
    assert rejected(run(POINTWISE, "R", "conclude"), "explicit")
    # a constant instance may be split, but that says nothing about other x
    result = run(POINTWISE, "R", "sub P: x:=1\nsplit [f(1)^2 = f(1)]")
    assert result.ok and not result.solved and len(result.state.branches) == 2


def test_pointwise_trap_splitnz_needs_a_constant():
    assert rejected(run(POINTWISE, "R", "splitnz f(x)"), "variables")


# --- Trap 2: cancelling f without injectivity --------------------------------

CONSTANT = "f(x + y) = f(x)"   # the solutions are exactly the constant functions


def test_cancel_requires_injectivity():
    """Cancelling f in f(x + y) = f(x) would give y = 0 for all y: 'no solutions'.
    But every constant function is a solution."""
    assert rejected(run(CONSTANT, "R", "cancel"), "injectivity has not been proven")
    assert rejected(run(CONSTANT, "R", "cancel P"), "injectivity")
    assert rejected(run(CONSTANT, "R", "inj"), "injective")      # and injectivity is not provable here
    good = run(CONSTANT, "R", "sub P: x:=0\nconclude")
    assert good.solved and good.solutions == parse_solution_set(["f(x) = c"])


def test_injectivity_is_not_granted_by_wishful_identities():
    assert rejected(run("f(f(x)) + y = x^2 + y", "R", "inj"), "injective")
    assert rejected(run("f(x + f(x)) + y = x + y", "R", "inj"), "injective")
    assert rejected(run("f(f(x)) + y = x*f(1) + y", "R", "inj"), "injective")  # f(1) might be 0


def test_injectivity_is_branch_local():
    """Injectivity proven under f(1) != 0 is not available in the case f(1) = 0."""
    problem = Problem.parse("f(f(x)) + y = x*f(1) + y", "R")
    state = initial_state(problem)
    state = apply(state, parse_move("splitnz f(1)"))
    # first case f(1) = 0: no injectivity
    with pytest.raises(Reject):
        apply(state, parse_move("inj"))
    assert "f(1) = 0" in state.current.case


# --- Trap 3: choosing a preimage without surjectivity ------------------------

def test_preimage_requires_surjectivity():
    """Picking a with f(a) = 0 for f(x + y) = f(x) would force the constant to be 0,
    losing every other constant solution."""
    assert rejected(run(CONSTANT, "R", "pre 0"), "surjectivity has not been proven")
    assert rejected(run(CONSTANT, "R", "surj"), "surjective")
    assert rejected(run(CONSTANT, "R", "sub P: x:=0\nonto R1: y"), "surjectivity")


def test_surjectivity_is_not_granted_by_wishful_identities():
    assert rejected(run("f(x + y) = f(x) + f(y)", "R", "surj"), "surjective")   # f = 0 is a solution
    assert rejected(run("f(f(x)) + y = x^2 + y", "R", "surj"), "surjective")
    assert rejected(run("f(x)f(y) + z = x + z", "R", "surj"), "surjective")       # a product, not a single f


def test_preimage_target_must_be_a_constant():
    """The witness a with f(a) = t depends on t, so t may not contain variables."""
    setup = "sub P: x:=0\nsurj\n"   # f(f(y)) = y + f(0): surjective
    eq = "f(x + f(y)) = f(x) + y"
    assert run(eq, "R", setup).ok
    assert rejected(run(eq, "R", setup + "pre x"), "variables")
    assert run(eq, "R", setup + "pre 0").ok


def test_witnesses_are_constants_not_variables():
    eq = "f(x + f(y)) = f(x) + y"
    assert rejected(run(eq, "R", "sub P: x:=a"), "unknown constant")          # no such witness yet
    setup = "sub P: x:=0\nsurj\npre 0\n"
    assert run(eq, "R", setup + "sub P: y:=a").ok                              # using it is fine
    # substituting FOR a witness is not even expressible in the text format ...
    with pytest.raises(ParseError):
        parse_move("sub P: a:=0")
    # ... and a hand-built move doing so is rejected by the checker
    state = run(eq, "R", setup).state
    with pytest.raises(Reject):
        apply(state, Subst("P", (("a", parse("0")),)))


def test_onto_requires_variable_only_inside_f():
    """Replacing f(y) by a free variable is only valid if y appears nowhere else."""
    eq = "f(x + f(y)) = f(x) + y"
    setup = "sub P: x:=0\nsurj\n"
    assert rejected(run(eq, "R", setup + "onto P: y"), "occurs outside")
    assert rejected(run(eq, "R", "onto P: y"), "surjectivity")


# --- Trap 4: dividing by something not proven nonzero -------------------------

IDEMPOTENT = "f(x)f(y) = f(x)"   # the solutions are f = 0 and f = 1


def test_division_requires_proven_nonzero():
    """Dividing f(0)f(y) = f(0) by f(0) loses the solution f = 0."""
    assert rejected(run(IDEMPOTENT, "R", "sub P: x:=0\ndiv [f(0)*f(y) = f(0)] by f(0)"), "not been proven nonzero")
    # the automatic simplifier must not do it silently either
    state = run(IDEMPOTENT, "R", "sub P: x:=0").state
    assert rejected(run(IDEMPOTENT, "R", "sub P: x:=0\nconclude"), "explicit")
    assert all("f(y) - 1" != str(r) for r in state.current.rows)
    # the honest proof treats f(0) = 0 separately and finds both solutions
    good = run(IDEMPOTENT, "R", "splitnz f(0)\nsub P: y:=0\nconclude\nsub P: x:=0\nconclude")
    assert good.solved and good.solutions == parse_solution_set(["f(x) = 0", "f(x) = 1"])


def test_division_by_a_variable_is_not_automatic():
    """x*f(x) = x gives f(x) = 1 only for x != 0; f(0) is unconstrained."""
    result = run("x*f(x) + y = x + y", "R", "conclude")
    assert rejected(result, "explicit")
    assert rejected(run("x*f(x) + y = x^2 + y", "R", "conclude"), "explicit")


def test_division_cannot_use_a_variable_or_unproven_term():
    assert rejected(run(IDEMPOTENT, "R", "div P by f(x)"), "variables")
    assert rejected(run(IDEMPOTENT, "R", "div P by 0"), "nonzero")


# --- Trap 5: additive does not imply linear over R ----------------------------

def test_cauchy_only_over_Q():
    """Over R there are additive functions that are not linear (Hamel bases)."""
    assert rejected(run("f(x + y) = f(x) + f(y)", "R", "cauchy"), "over R")
    assert not run("f(x + y) = f(x) + f(y)", "R", "").solved
    good = run("f(x + y) = f(x) + f(y)", "Q", "cauchy\nconclude")
    assert good.solved and good.solutions == parse_solution_set(["f(x) = c*x"])


def test_cauchy_needs_an_additive_identity():
    assert rejected(run("f(x + y) = f(x) + y", "Q", "cauchy"), "f(x + y) = f(x) + f(y)")
    # a defect that is not of the form p(x + y) - p(x) - p(y) is refused
    assert rejected(run("f(x + y) = f(x) + f(y) + x^2*y", "Q", "cauchy"))
    assert rejected(run("f(x + y) = f(x) + f(y) + f(x)f(y)", "Q", "cauchy"))


# --- Trap 6: case splits must be exhaustive and every case must close ---------

PRODUCT = "f(x)f(y) = f(x+y) + xy"
SETUP = "sub P: x:=0, y:=0\n"   # f(0)^2 = f(0)


def test_split_must_be_exhaustive():
    assert rejected(run(PRODUCT, "R", SETUP + "split [f(0)^2 = f(0)] by f(0)"), "not exhaustive")
    assert rejected(run(PRODUCT, "R", SETUP + "split [f(0)^2 = f(0)] by f(0), f(0) - 2"), "exhaustive")
    assert rejected(run(PRODUCT, "R", SETUP + "split [f(0)^2 = f(0)] by f(0), 2"))
    assert run(PRODUCT, "R", SETUP + "split [f(0)^2 = f(0)] by f(0), f(0) - 1").ok


def test_split_on_unknown_fact_is_refused():
    assert rejected(run(PRODUCT, "R", "split [f(0)^2 = f(0)]"), "not known")
    assert rejected(run(PRODUCT, "R", SETUP + "split [f(0) = 1]"), "not known")
    assert rejected(run(PRODUCT, "R", SETUP + "split [f(1) = f(1)]"))


def test_every_case_must_be_closed():
    """Handling only the case f(0) = 0 and stopping is not a proof."""
    result = run(PRODUCT, "R", SETUP + "split [f(0)^2 = f(0)]\nsub P: y:=0\nconclude")
    assert result.ok and not result.solved and result.solutions is None
    assert "open" in result.error


# --- Trap 7: claimed solutions are substituted back ---------------------------

def test_wrong_solutions_fail_verification():
    problem = Problem.parse("f(x + f(y)) = f(x) + y", "Q")
    assert verify_solution(problem, "f(x) = x") and verify_solution(problem, "f(x) = -x")
    assert not verify_solution(problem, "f(x) = 2x")
    assert not verify_solution(problem, "f(x) = x + 1")
    assert not verify_solution(problem, "f(x) = c*x")     # true for some c only


def test_concluded_candidates_are_filtered_by_the_original_equation():
    """f(x) = 1 follows from P(x, 0), but it does not satisfy the equation: no solutions."""
    result = run("f(x) + f(x+y) = y + 2", "R", "sub P: y:=0\nconclude")
    assert result.solved and len(result.solutions) == 0
    """f(x) = x*f(1) follows, but only f(1) = +-1 survives substitution."""
    result = run("f(x*f(y)) = xy", "R", "sub P: x:=1\nsub P: y:=f(y)\nsub [f(xy) = x*f(y)]: y:=1\nconclude")
    assert result.solved and result.solutions == parse_solution_set(["f(x) = x", "f(x) = -x"])


def test_irrational_constants_are_refused_not_dropped():
    """f(x)f(1) = 2x forces f(1)^2 = 2. Over Q that is a contradiction; over R it
    is not (f(x) = +-sqrt(2) x), and since v1 cannot express sqrt(2) the checker
    must leave the case open rather than report 'no solutions'."""
    over_q = check(Problem.parse("f(x)*f(1) + y = 2x + y", "Q"), parse_proof("sub P: x:=1"))
    assert over_q.solved and len(over_q.solutions) == 0       # f(1)^2 = 2: impossible in Q
    over_r = check(Problem.parse("f(x)*f(1) + y = 2x + y", "R"), parse_proof("sub P: x:=1"))
    assert over_r.ok and not over_r.solved                    # possible in R: not a contradiction
    # concluding f(x) = c*x with c^2 = 2 is refused with an explanation
    stuck = run("f(x*f(y)) = 2xy", "R", "sub P: y:=1\nsub P: x:=1\nsub P: x:=1, y:=1")
    assert stuck.ok and not stuck.solved


# --- Traps around the square lemmas (sqadd, sqlin) --------------------------

def test_additive_on_sums_of_two_squares_is_not_additive():
    """f(x^2 + y^2) = f(x^2) + f(y^2) holds for f(t) = |t|, which is not additive.
    Only f(x^2 + y) = f(x^2) + f(y), with a free second argument, gives additivity."""
    assert rejected(run("f(x^2 + y^2) = f(x^2) + f(y^2)", "R", "sqadd"), "neither")
    assert rejected(run("f(x^2 + y^2) = f(x^2) + f(y^2)", "Q", "sqadd"), "neither")
    assert run("f(x^2 + y) = f(x^2) + f(y)", "R", "sqadd").ok
    assert run("f(x^2 + y) = f(x^2) + f(y)", "Q", "sqadd").ok


def test_the_difference_of_squares_form_needs_real_square_roots():
    """Over R every u >= 0 is a square, so f(x^2 - y^2) = f(x^2) - f(y^2) says f(u - v) = f(u) - f(v) for
    u, v >= 0. Over Q it only speaks about rational squares, and the move is refused."""
    assert run("f(x^2 - y^2) = f(x^2) - f(y^2)", "R", "sqadd").ok
    assert rejected(run("f(x^2 - y^2) = f(x^2) - f(y^2)", "Q", "sqadd"), "neither")


def test_sqadd_needs_f_of_a_square_not_the_square_of_f():
    """f(x^2 + y) = f(x)^2 + f(y) alone is not the hypothesis. With f(x^2) = f(x)^2 also known, it is."""
    equation = "f(x^2 + y) = f(x)^2 + f(y)"
    assert rejected(run(equation, "R", "sqadd"), "neither")
    result = run(equation, "R", "sub P: y:=0\nsub P: x:=0, y:=0\nsqadd")      # f(0) = 0, then f(x^2) = f(x)^2
    assert result.ok and "additive" in result.state.current.props


def test_sqlin_needs_additivity_and_a_genuine_square():
    """The sign information comes from f(x^2) = f(x)^2 >= 0. f(x^2) = x f(x) carries none, and without
    additivity nothing follows at all (f = 1 satisfies f(x^2) = f(x)^2)."""
    assert rejected(run("f(x^2) = f(x)^2", "R", "sqlin"), "not known to be additive")
    assert rejected(run("f(x^2 - y^2) = x*f(x) - y*f(y)", "R", "sub P: y:=0\nsqadd\nsqlin"), "f(x^2) = f(x)^2 is not known")
    assert rejected(run("f(x^2 + y) = f(x^2) + f(y)", "R", "sqadd\nsqlin"), "f(x^2) = f(x)^2 is not known")
    assert rejected(run("f(x^2 + y) = f(x)^2 + f(y)", "Q", "sub P: y:=0\nsub P: x:=0, y:=0\nsqadd\nsqlin"), "over Q")
    result = run("f(x^2 + y) = f(x)^2 + f(y)", "R", "sub P: y:=0\nsub P: x:=0, y:=0\nsqadd\nsqlin\nconclude")
    assert result.solved and result.solutions == parse_solution_set(["f(x) = 0", "f(x) = x"])


def test_the_square_lemmas_take_no_target_and_do_not_solve_cauchy_over_r():
    assert rejected(run("f(x^2 + y) = f(x^2) + f(y)", "R", "sqadd P"), "takes no target")
    assert rejected(run("f(x+y) = f(x) + f(y)", "R", "sqadd"), "already known to be additive")
    assert rejected(run("f(x+y) = f(x) + f(y)", "R", "sqlin"), "f(x^2) = f(x)^2 is not known")
    from alphafe.env import start

    state, _ = start(Problem.parse("f(x+y) = f(x) + f(y)", "R"))     # Cauchy over R must stay open
    assert not state.solved


# --- Trap: what counts as proven nonzero -------------------------------------

def test_products_of_nonzero_constants_are_nonzero_and_nothing_else_is():
    """c != 0 gives c^2 != 0 and, with d != 0, cd != 0. It gives nothing about a constant that was never
    assumed nonzero, and a nonzero product makes each factor nonzero."""
    equation = "f(f(x) + y) = f(1)^2*x + f(y) + f(1)^2 - 1"
    result = run(equation, "R", "sub P: x:=1, y:=1\nsplitnz f(1)")
    branch = result.state.current
    from alphafe.algebra import parse_poly as P

    assert branch.known_nonzero(P("f(1)")) and branch.known_nonzero(P("f(1)^2")) and branch.known_nonzero(P("-3f(1)^3"))
    assert not branch.known_nonzero(P("f(2)")) and not branch.known_nonzero(P("f(1)*f(2)"))
    assert not branch.known_nonzero(P("f(1) + 1")) and not branch.known_nonzero(P("f(1)^2 - 1"))
    # With the coefficient f(1)^2 recognised, injectivity and surjectivity follow (they were refused before).
    assert run(equation, "R", "sub P: x:=1, y:=1\nsplitnz f(1)\ninj\nsurj").ok
    # The other direction: a nonzero product makes its factors nonzero.
    after = run(equation, "R", "sub P: x:=1, y:=1\nsplitnz f(1)^2").state.current
    assert after.known_nonzero(P("f(1)")) and not after.known_nonzero(P("f(2)"))
    # Division is still refused by a constant that is merely not known to vanish.
    assert rejected(run("f(x)*f(0) = x*f(0)", "R", "div P by f(0)"))
