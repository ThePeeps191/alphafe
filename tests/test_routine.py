"""The routine substitutions the environment applies by itself (alphafe.env.routine_moves).

They are ordinary ``sub`` moves, so nothing here can make the checker accept
more than it did. What needs testing is that they are recorded and replay,
that they stop, that they never contradict a known solution, and that a
found proof can be cut back to the moves it uses.
"""

import random
import zlib

import pytest

from alphafe import env
from alphafe import terms as T
from alphafe.algebra import poly_term
from alphafe.checker import Problem, Reject, check, initial_state
from alphafe.env import close, close_free, creative_moves, minimise, prune, quote_targets, start, step
from alphafe.modelcheck import check_state
from alphafe.moves import Inj, Subst, parse_move, parse_proof, show_move
from alphafe.solutions import parse_solution_set, verify

from .seedlib import expected, load_seeds, seed_problem
from .test_modelcheck import instantiate, random_move

SEEDS = load_seeds()


@pytest.mark.parametrize("record", SEEDS, ids=[r["id"] for r in SEEDS])
def test_start_is_a_checked_proof_prefix_that_keeps_every_solution(record):
    problem = seed_problem(record)
    state, proof = start(problem)
    result = check(problem, proof)
    assert result.ok                                        # every routine move is accepted when replayed
    assert result.state.key() == state.key()                # ... and replaying gives the same state
    if state.solved:
        assert state.solution_set == expected(record)
    rng = random.Random(zlib.crc32(record["id"].encode()))
    for solution in record["solutions"]:
        expr = instantiate(solution, rng)
        assert verify(problem.poly, expr)
        check_state(state, expr, rng)                       # no identity, property or case contradicts it


def test_routine_moves_are_plain_substitutions_recorded_in_the_proof():
    problem = Problem.parse("f(x+y) = f(x) + y")
    state, proof = start(problem)
    assert state.solved and state.solution_set == parse_solution_set(["f(x) = x + c"])
    assert any(isinstance(move, Subst) for move in proof)   # an opening substitution did the work
    assert all(isinstance(move, Subst) or move in env.FREE_MOVES for move in proof)
    # With the routine substitutions off, only the free moves run and the problem stays open.
    bare, moves = close_free(initial_state(problem))
    assert not bare.solved and all(move in env.FREE_MOVES for move in moves)


def test_switches_turn_each_kind_off(monkeypatch):
    problem = Problem.parse("f(x+y) = f(x) + y")
    for name in env.ROUTINE:
        monkeypatch.setitem(env.ROUTINE, name, False)
    state, proof = start(problem)
    assert not state.solved and all(move in env.FREE_MOVES for move in proof)
    monkeypatch.setitem(env.ROUTINE, "swap", True)
    _, proof = start(Problem.parse("f(x + f(y)) = f(x) + y", "Q"))
    assert parse_move("sub P: x:=y, y:=x") in proof


def test_the_opening_substitutions_come_in_three_groups(monkeypatch):
    """Zeros and diagonals, then 1 and -1, then f of a variable. IMO 1992/2 needs the last group and nothing else."""
    problem = Problem.parse("f(x^2 + f(y)) = y + f(x)^2")
    state, proof = start(problem)
    assert state.solved and state.solution_set == parse_solution_set(["f(x) = x"])
    assert parse_move("sub P: x:=f(x)") in proof and check(problem, proof).solved
    monkeypatch.setitem(env.ROUTINE, "fterms", False)
    state, proof = start(problem)
    assert not state.solved and parse_move("sub P: x:=f(x)") not in proof and parse_move("sub P: x:=1") in proof
    monkeypatch.setitem(env.ROUTINE, "ones", False)
    _, proof = start(problem)
    assert parse_move("sub P: x:=1") not in proof and parse_move("sub P: x:=0") in proof
    monkeypatch.setitem(env.ROUTINE, "opening", False)
    _, proof = start(problem)
    assert parse_move("sub P: x:=0") not in proof


def test_instances_do_not_feed_themselves():
    """IMO 2019/1 over Q. f(f(x)) = 2f(x) + f(0) taken at x := f(0), then at the new argument, and so on,
    would produce f(3f(0)), f(7f(0)), ... without end. An instance may not introduce a new f(...)."""
    problem = Problem.parse("f(2x) + 2f(y) = f(f(x+y))", "Q")
    state, proof = start(problem)
    assert check(problem, proof).ok
    for branch in state.branches:
        assert len(branch.rows) < 25
        for row in branch.rows:
            assert T.nesting_depth(poly_term(row)) <= 2         # nothing deeper than the f(f(...)) of the equation


def test_one_call_applies_a_bounded_number_of_routine_moves(monkeypatch):
    problem = Problem.parse("f(x + f(y)) = f(x) + y", "Q")
    for cap in (0, 1, 3):
        monkeypatch.setattr(env, "MAX_ROUTINE", cap)
        _, moves = close(initial_state(problem))
        assert sum(isinstance(move, Subst) for move in moves) <= cap


def test_a_named_witness_is_put_into_the_equation():
    problem = Problem.parse("f(f(x) + y) = x + f(y)", "Q")
    state, _ = close_free(initial_state(problem))
    assert "surjective" in state.current.props
    state, applied = step(state, parse_move("pre 0"))
    assert applied[0] == parse_move("pre 0")
    assert any(isinstance(m, Subst) and m.target == "P" and "a" in show_move(m) for m in applied[1:]) or state.solved


@pytest.mark.parametrize("record", SEEDS[::4], ids=[r["id"] for r in SEEDS[::4]])
def test_random_moves_through_the_environment_never_contradict_a_known_solution(record):
    """The model-check fuzzer, run through env.step so that the routine moves are fuzzed too."""
    problem = seed_problem(record)
    rng = random.Random(zlib.crc32(("env:" + record["id"]).encode()))
    for solution in record["solutions"]:
        expr = instantiate(solution, rng)
        state, _ = start(problem)
        check_state(state, expr, rng)
        for _ in range(25):
            if state.solved:
                break
            try:
                state, _ = step(state, random_move(rng, state))
            except Reject:
                continue
            check_state(state, expr, rng)


def test_creative_moves_recovers_what_the_search_proposed():
    from alphafe.baseline.search import brute_force

    problem = Problem.parse("f(x)f(y) = f(x+y) + xy")           # seed s33: two nested case splits
    result = brute_force(problem, max_calls=20000, max_seconds=60)
    assert result.solved
    proposed = creative_moves(problem, result.proof)
    assert proposed is not None and 0 < len(proposed) < len(result.proof)
    assert all(move not in env.FREE_MOVES for move in proposed)
    # A proof that the environment did not produce has no such reading.
    assert creative_moves(problem, parse_proof("sub P: y:=1\nsub P: x:=0")) is None


def test_prune_keeps_the_answer_and_drops_what_is_not_used():
    problem = Problem.parse("f(x+y) = f(x) + y")
    state, proof = start(problem)
    assert state.solved and Inj() not in prune(problem, proof)      # nothing here uses injectivity
    short = prune(problem, proof)
    assert check(problem, short).solved and check(problem, short).solutions == state.solution_set
    assert len(short) <= 3 and prune(problem, short) == short
    for index in range(len(short)):                                 # every remaining move is needed
        assert not check(problem, short[:index] + short[index + 1:]).solved
    # Not a complete proof: returned as it is.
    partial = parse_proof("sub P: y:=1")
    assert prune(problem, partial) == partial


def test_quoted_targets_survive_the_removal_of_earlier_moves():
    problem = Problem.parse("f(x+f(y)) = f(x) + y", "Q")
    proof = parse_proof("sub P: x:=0\nsub P: y:=0\nsub R5: x:=y")     # R5 is the original equation at this point
    assert check(problem, proof).ok
    quoted = quote_targets(problem, proof)
    assert check(problem, quoted).ok and show_move(quoted[2]).startswith("sub [")
    assert check(problem, quoted).state.key() == check(problem, proof).state.key()
    # Without the first move there are only three identities: R5 is gone, the quoted identity is not.
    assert not check(problem, proof[1:]).ok
    assert check(problem, quoted[1:]).ok


@pytest.mark.parametrize("record", SEEDS[::5], ids=[r["id"] for r in SEEDS[::5]])
def test_minimise_gives_a_shorter_checked_proof_of_the_same_answer(record):
    from alphafe.baseline.search import brute_force

    problem = seed_problem(record)
    result = brute_force(problem, max_calls=3000, max_seconds=30)
    if not result.solved:
        pytest.skip("not solved within this small budget")
    short = minimise(problem, result.proof)
    verdict = check(problem, short)
    assert verdict.solved and verdict.solutions == expected(record) and len(short) <= len(result.proof)
