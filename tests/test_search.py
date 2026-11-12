import random

import pytest

from alphafe.checker import Problem, check
from alphafe.search import BestFirstSearch, GreedySearch, UniformProposer, run_searches
from alphafe.solutions import parse_solution_set

pytestmark = pytest.mark.usefixtures("plain_environment")      # see tests/conftest.py


def solve(search_cls, equation, domain="R", budget=200, seed=0):
    search = search_cls(Problem.parse(equation, domain), budget=budget)
    run_searches([search], UniformProposer(random.Random(seed)), k=8)
    return search


def test_best_first_solves_and_the_proof_rechecks():
    search = solve(BestFirstSearch, "f(x+y) = f(x) + y")
    result = search.result()
    assert result.solved and result.solutions == parse_solution_set(["f(x) = x + c"])
    assert check(search.problem, result.proof).solved
    assert result.checker_calls <= 200 and result.source == "network-search"
    path = search.solution_path()
    assert path[0] is search.root and path[-1] is search.solved_node
    assert all(node.move_ids is not None for node in path[1:])


def test_greedy_never_backtracks():
    search = solve(GreedySearch, "f(x+y) = f(x) + y", budget=100)
    assert search.result().source == "network-greedy"
    node = search.current
    length = 0                          # counted by hand: node.depth starts again whenever a case closes
    while node.parent is not None:      # a single chain from the root
        node = node.parent
        length += 1
    assert node is search.root and len(search.nodes) == length + 1


def test_budget_is_respected_and_failure_is_reported():
    search = solve(BestFirstSearch, "f(x-y) = f(x)f(y)", "R", budget=40)
    result = search.result()
    assert not result.solved and result.checker_calls <= 40 and result.proof == [] and result.reason


def test_trivial_problem_needs_no_calls():
    search = BestFirstSearch(Problem.parse("f(x+y) = f(x) + f(y)", "Q"), budget=10)
    assert search.done and search.result().solved and search.result().checker_calls == 0


def test_many_searches_advance_together():
    problems = [Problem.parse(e) for e in ["f(x+y) = f(x) + y", "f(xy) = x*f(y)", "f(x) + f(y) = x + y"]]
    searches = [BestFirstSearch(p, budget=300) for p in problems]
    run_searches(searches, UniformProposer(random.Random(2)), k=8)
    assert all(s.done for s in searches) and sum(s.solved_node is not None for s in searches) == 3


def test_value_guided_search_still_solves():
    search = BestFirstSearch(Problem.parse("f(x+y) = f(x) + y"), budget=300, value_weight=1.0)
    run_searches([search], UniformProposer(random.Random(0)), k=8)
    assert search.result().solved and not search.unvalued


def test_search_commits_when_a_case_closes():
    """After a case split, closing a case discards the rest of the frontier."""
    search = BestFirstSearch(Problem.parse("f(x)f(y) = f(xy) + x + y"), budget=3000)
    run_searches([search], UniformProposer(random.Random(3)), k=8)
    assert search.result().solved and search.commits >= 1
    assert search.result().solutions == parse_solution_set(["f(x) = x + 1"])


class Scripted:
    """A proposer that reads its proposals for each round from a list (the last entry repeats)."""

    def __init__(self, rounds):
        self.rounds, self.asked = rounds, 0

    def propose(self, views, k):
        from alphafe.moves import parse_move
        from alphafe.tokenizer import encode_move

        texts = self.rounds[min(self.asked, len(self.rounds) - 1)]
        self.asked += 1
        return [[(encode_move(parse_move(text), view), -float(i)) for i, text in enumerate(texts)] for view in views]


def test_a_move_is_sent_once_per_state_and_a_state_with_nothing_new_is_dropped():
    # x := x makes nothing new, so the checker refuses it. Proposed for ever, it costs one call.
    search = BestFirstSearch(Problem.parse("f(x-y) = f(x)f(y)", "R"), budget=50)
    run_searches([search], Scripted([["sub P: x:=x"]]), k=8)
    result = search.result()
    assert not result.solved and result.checker_calls == 1 and result.reason == "frontier empty"
    greedy = GreedySearch(Problem.parse("f(x-y) = f(x)f(y)", "R"), budget=50)
    run_searches([greedy], Scripted([["sub P: x:=x"]]), k=8)
    assert greedy.result().checker_calls == 1 and greedy.result().reason == "no proposal was accepted"


def test_a_state_stays_on_the_frontier_while_it_yields_new_moves():
    # Ten rounds of a different refused move each, then the move that solves: no fixed number of visits ends the search.
    refused = [[f"sub P: x:=x, y:=y + {n} - {n}"] for n in range(1, 11)]
    search = BestFirstSearch(Problem.parse("f(x+y) = f(x) + y", "R"), budget=50)
    run_searches([search], Scripted(refused + [["sub P: x:=0"]]), k=8)
    assert search.result().solved and search.root.expansions == 11
