"""An equation over the checker's size caps is reported as not solved everywhere; nothing raises or hangs.

The caps (80 monomials, structural size 400) apply to every identity, the
original equation included. `(x+y)^20` expands to 22 monomials of size 444.
"""

import random

import pytest

from alphafe.baseline.guesser import guess
from alphafe.baseline.search import brute_force
from alphafe.bench import BenchProblem
from alphafe.checker import LOAD_REFUSED, Problem, Reject, check
from alphafe.cli import main
from alphafe.env import start, try_start
from alphafe.eval import run_baseline, run_policy
from alphafe.search import BestFirstSearch, GreedySearch, UniformProposer, run_searches

BIG = "f(x+y) = (x+y)^20"
HUGE = "f(x^2015 + f(y)^2015) = f(x)^2015 + y^2015"       # Korean MO 2015/1, in benchmarks/real


def test_check_returns_a_verdict_for_an_equation_it_cannot_load():
    result = check(Problem.parse(BIG), [])
    assert not result.ok and not result.solved and result.solutions is None
    assert result.error.startswith(LOAD_REFUSED) and str(result).startswith("not checked")
    # One monomial fewer loads normally.
    assert check(Problem.parse("f(x+y) = (x+y)^18"), []).ok


def test_start_raises_and_try_start_reports():
    with pytest.raises(Reject):
        start(Problem.parse(BIG))
    state, moves, why = try_start(Problem.parse(BIG))
    assert state is None and moves == [] and why.startswith(LOAD_REFUSED)
    state, moves, why = try_start(Problem.parse("f(x+y) = f(x) + y"))
    assert state is not None and why == ""


@pytest.mark.parametrize("equation", [BIG, HUGE])
def test_every_solver_scores_it_as_unsolved(equation):
    problem = Problem.parse(equation)
    result = brute_force(problem, max_calls=50, max_seconds=5)
    assert not result.solved and result.checker_calls == 0 and result.reason.startswith(LOAD_REFUSED)
    searches = [GreedySearch(problem, budget=8), BestFirstSearch(problem, budget=8),
                BestFirstSearch(Problem.parse("f(x+y) = f(x) + y"), budget=64)]
    run_searches(searches, UniformProposer(random.Random(0)), k=4)      # must return: the first two have nothing to expand
    for search in searches[:2]:
        result = search.result()
        assert search.request() is None and not result.solved and result.checker_calls == 0
        assert result.reason.startswith(LOAD_REFUSED) and search.solution_path() == []
    bench = BenchProblem("big", problem, None, 10)
    for row in run_baseline([bench], 50, 5, workers=1) + run_policy([bench], UniformProposer(random.Random(0)), "search", 8):
        assert not row.solved and row.reason.startswith(LOAD_REFUSED)


def test_the_guess_declines_a_huge_exponent_instead_of_expanding_it():
    found = guess(Problem.parse(HUGE))
    assert found.solutions is None and found.exponent == 2015 and "2015" in str(found)
    assert guess(Problem.parse("f(x+y) = f(x) + y")).exponent == 0


@pytest.mark.parametrize("equation", [BIG, HUGE])
def test_the_command_line_says_so_without_a_traceback(equation, tmp_path, capsys):
    assert main(["solve", equation, "--baseline", "--baseline-budget", "50", "--seconds", "5"]) == 1
    assert LOAD_REFUSED in capsys.readouterr().out
    proof = tmp_path / "p.proof"
    proof.write_text("sub P: y:=0\n")
    assert main(["check", equation, "--proof", str(proof)]) == 1
    assert "not checked" in capsys.readouterr().out
