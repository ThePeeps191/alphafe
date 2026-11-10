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
