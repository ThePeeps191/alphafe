import pytest

from alphafe.checker import Problem, check
from alphafe.moves import parse_proof
from alphafe.render import render

from .seedlib import seed_problem, seed_proofs


@pytest.mark.parametrize("record, proof", seed_proofs(), ids=lambda v: v["id"] if isinstance(v, dict) else "")
def test_every_seed_proof_renders(record, proof):
    text = render(seed_problem(record), proof)
    assert text.startswith("Problem. Find all functions f:")
    assert "Answer." in text and "All cases are closed" in text
    assert "REJECTED" not in text and "INCOMPLETE" not in text
    assert "k0" not in text and "#" not in text      # internal names never leak


def test_render_simple_proof_reads_naturally():
    problem = Problem.parse("f(x+y) = f(x) + y", "R")
    text = render(problem, parse_proof("sub P: x:=0\nconclude"))
    assert "Let P(x, y) denote the assertion f(x+y) = f(x) + y." in text
    assert "P(0, y) gives f(y) = y + f(0)." in text
    assert "Hence f(x) = x + f(0) for all x." in text
    assert "Answer. f(x) = x + c for any constant c." in text


def test_render_cases():
    problem = Problem.parse("f(x)f(y) = f(xy) + x + y", "R")
    text = render(problem, parse_proof("sub P: x:=0, y:=0\nsplit [f(0)^2 = f(0)]\nsub P: y:=0\nsub P: y:=0\nconclude"))
    assert "we have f(0) = 0 or f(0) = 1" in text
    assert "Case f(0) = 0." in text and "So this case is impossible." in text
    assert "Case f(0) = 1." in text


def test_render_never_presents_a_bad_proof_as_a_proof():
    problem = Problem.parse("f(x+y) = f(x)", "R")
    rejected = render(problem, parse_proof("cancel"))
    assert "REJECTED" in rejected and "Answer." not in rejected
    incomplete = render(Problem.parse("f(x+y) = f(x) + y", "R"), parse_proof("sub P: x:=0"))
    assert "INCOMPLETE" in incomplete and "Answer." not in incomplete


def solution_lines(equation, proof, domain="R"):
    from alphafe.checker import Problem
    from alphafe.moves import parse_proof
    from alphafe.render import render

    return render(Problem.parse(equation, domain), parse_proof(proof)).splitlines()


def test_a_case_says_what_the_relations_become_before_concluding():
    """The line after a case heading used to be a bare "Hence f(x) = ..." (issue #84)."""
    lines = solution_lines("f(x)f(y) = f(xy) + x + y", "sub P: x:=0\nsub R1: x:=0\nsplit R1\nconclude")
    at = lines.index("Case f(0) = 1.")
    assert lines[at + 1].startswith("With this, the relations above become: f(x) = x + 1")
    assert lines[at + 2] == "Hence f(x) = x + 1 for all x."


def test_a_substitution_is_shown_as_substituted():
    """The printed result used to be rewritten with the identity substituted into, so it could contain the
    variable that had just been replaced (issue #85)."""
    lines = solution_lines("f(x^2) - f(y^2) = (x+y)(f(x) - f(y))", "sub R1: x:=0\nsub P: y:=2\nconclude")
    first = next(line for line in lines if line.startswith("Putting x = 0"))
    assert first.endswith("gives f(y^2) = yf(y) - f(0)y + f(0).")
    lines = solution_lines("f(x+y) + 2f(x-y) = 3f(x) - y", "sub P: x:=0\nsub R1: x:=-x\nconclude")
    at = next(i for i, line in enumerate(lines) if line.startswith("Putting x = -x"))
    assert lines[at + 1] == "With the relations already known, this becomes f(x) = x + f(0)."      # no factor 3/4


def test_a_cancellation_names_both_identities_it_compares():
    """Injectivity was applied to one equation that is not of the form f(A) = f(B) (issue #86)."""
    proof = "inj\nsub P: y:=0\nsub P: x:=0\nsub R2: y:=0\ncancel\nsub R3: y:=x\ncancel\nconclude"
    text = "\n".join(solution_lines("f(x + f(y) + z) = x + y + f(z)", proof))
    assert ("The relations f(x + z) = f(z) + x and f(f(x) + z) = f(z) + x give the same value of f at two arguments. "
            "Since f is injective, the arguments are equal: f(x) = x.") in text
    assert "Since f is injective, f(x + f(0)) = f(x) gives f(0) = 0." in text      # one identity is enough here
