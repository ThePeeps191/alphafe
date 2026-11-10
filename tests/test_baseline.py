import pytest

from alphafe.baseline.guesser import guess
from alphafe.baseline.search import brute_force, candidate_moves
from alphafe.bench import AnswerMismatch, BenchProblem, canary, load_real, load_seed
from alphafe.checker import Problem, check
from alphafe.env import FREE_MOVES, confirm, start, step
from alphafe.eval import by_mohs, run_baseline, score, summary
from alphafe.moves import Conclude, parse_move
from alphafe.solutions import parse_solution_set


def test_guesser_finds_polynomial_answers():
    assert guess(Problem.parse("f(x+y) = f(x) + y")).solutions == parse_solution_set(["f(x) = x + c"])
    assert guess(Problem.parse("f(x + f(y)) = f(x) + y", "Q")).solutions == parse_solution_set(["f(x) = x", "f(x) = -x"])
    assert guess(Problem.parse("f(x+y) - f(x-y) = 4xy")).solutions == parse_solution_set(["f(x) = x^2 + c"])
    assert len(guess(Problem.parse("f(x) + f(x+y) = y + 2")).solutions) == 0


def test_guesser_is_only_a_guess():
    """The guesser misses non-quadratic answers; it proves nothing about completeness."""
    cubic = Problem.parse("(x-y)f(x+y) - (x+y)f(x-y) = 4xy(x^2 - y^2)")
    assert guess(cubic).solutions != parse_solution_set(["f(x) = x^3 + c*x"])


def test_free_moves_close_easy_states():
    problem = Problem.parse("f(x+y) = f(x) + f(y)", "Q")
    state, proof = start(problem)                      # cauchy + conclude are free
    assert state.solved and confirm(problem, proof) == parse_solution_set(["f(x) = c*x"])
    problem = Problem.parse("f(x+y) = f(x) + y")
    state, proof = start(problem)
    # nothing creative is free here (surjectivity is: f(x + y) = f(x) + y shows it)
    assert not state.solved and all(m in FREE_MOVES for m in proof)
    state, applied = step(state, parse_move("sub P: x:=0"))
    assert state.solved and applied[-1] == Conclude()


def test_brute_force_solves_easy_problems_and_proofs_recheck():
    for equation, domain, answer in [
        ("f(x+y) = f(x) + y", "R", ["f(x) = x + c"]),
        ("f(x)f(y) = f(xy) + x + y", "R", ["f(x) = x + 1"]),
        ("f(f(x) + f(y)) = x + y", "Q", ["f(x) = x", "f(x) = -x"]),
    ]:
        problem = Problem.parse(equation, domain)
        result = brute_force(problem, max_calls=3000, max_seconds=30)
        assert result.solved and result.source == "baseline"
        assert result.solutions == parse_solution_set(answer)
        assert check(problem, result.proof).solved          # independent re-check


def test_brute_force_respects_its_budget():
    problem = Problem.parse("f(x-y) = f(x)f(y)", "R")
    result = brute_force(problem, max_calls=150, max_seconds=30)
    assert not result.solved and result.checker_calls <= 150 and result.proof == []


def test_brute_force_does_not_solve_what_cannot_be_expressed():
    """Cauchy over R has non-polynomial solutions; no proof may be found."""
    result = brute_force(Problem.parse("f(x+y) = f(x) + f(y)", "R"), max_calls=400, max_seconds=30)
    assert not result.solved


def test_candidate_moves_only_use_available_symbols():
    state, _ = start(Problem.parse("f(x+y) = f(x) + y"))
    shown = " ".join(str(m) for m in candidate_moves(state))
    assert "Sym(name='a')" not in shown and "Var(name='z')" not in shown


def test_benchmark_loading_and_canary():
    seeds = load_seed()
    assert len(seeds) >= 40 and all(b.expected is not None and b.source == "seed" for b in seeds)
    assert load_real() == []                                 # owners add these later
    bench = seeds[0]
    canary(bench, bench.expected)
    with pytest.raises(AnswerMismatch):
        canary(bench, parse_solution_set(["f(x) = 2x"]))


def test_eval_scoring():
    seeds = load_seed()[:4]
    rows = run_baseline(seeds, max_calls=300, max_seconds=20, workers=1)
    assert all(r.solved for r in rows)
    s = summary(rows)
    assert s["solved"] == 4 and s["rate"] == 1.0
    assert by_mohs(rows) == {"0M": [4, 4]}
