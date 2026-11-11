"""Version 1 covers equations in 2 or 3 variables; these tests exercise the third."""

import random

from alphafe.baseline.search import brute_force
from alphafe.checker import Problem, apply, initial_state
from alphafe.env import start
from alphafe.moves import parse_move
from alphafe.search import BestFirstSearch, UniformProposer, run_searches
from alphafe.solutions import parse_solution_set
from alphafe.tokenizer import MoveGrammar, TOKEN_ID, decode_move, encode_move, encode_state, sample_uniform

from .seedlib import load_seeds, seed_problem
import pytest

pytestmark = pytest.mark.usefixtures("plain_environment")      # see tests/conftest.py

THREE = [s for s in load_seeds() if len(seed_problem(s).poly.variables()) == 3]


def test_there_are_three_variable_seeds():
    assert len(THREE) >= 3


def test_one_variable_identities_are_renamed_to_all_three_names():
    state = initial_state(Problem.parse("f(x + y + z) = f(x) + y + z"))
    state = apply(state, parse_move("sub P: x:=0, z:=0"))
    rows = {str(r) for r in state.current.rows}
    assert {"f(x) - x - f(0)", "f(y) - y - f(0)", "f(z) - z - f(0)"} <= rows


def test_grammar_can_bind_z():
    state, _ = start(Problem.parse("f(x + f(y) + z) = x + y + f(z)"))
    view = encode_state(state)
    assert view.p_vars == ["x", "y", "z"]
    move = parse_move("sub P: x:=-f(y) - z, z:=0")
    ids = encode_move(move, view)
    assert ids is not None and TOKEN_ID["z"] in ids
    assert encode_move(decode_move(ids, view), view) == ids
    grammar = MoveGrammar(view)
    for token in ids:                      # the grammar accepts exactly this move
        grammar.advance(token)
    assert grammar.done
    rng = random.Random(0)
    assert any(TOKEN_ID["z"] in sample_uniform(view, rng)[0] for _ in range(200))


def test_brute_force_solves_three_variable_seeds():
    for record in THREE:
        result = brute_force(seed_problem(record), max_calls=3000, max_seconds=60)
        assert result.solved, record["equation"]
        assert result.solutions == parse_solution_set(record["solutions"])


def test_policy_search_solves_a_three_variable_seed():
    search = BestFirstSearch(Problem.parse("f(x + y + z) = f(x) + y + z"), budget=400)
    run_searches([search], UniformProposer(random.Random(1)), k=8)
    assert search.result().solved
