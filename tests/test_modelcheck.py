"""Model-check fuzzing: random legal moves must never contradict a known solution.

For every seed problem and every expected solution (with random parameter
values), we fire random moves at the checker. Whatever it accepts, the
resulting state is tested against the known solution: every derived identity
must hold for it, every property claimed must be true of it, and it must
never be lost by a case split or a conclusion.
"""

import random
import zlib
from fractions import Fraction

import pytest

from alphafe import terms as T
from alphafe.algebra import Poly, parse_poly
from alphafe.checker import Reject, apply, initial_state
from alphafe.modelcheck import Unsound, check_state
from alphafe.moves import Cancel, Cauchy, Conclude, Divide, Inj, Onto, Pre, Quadratic, Split, SplitNZ, Subst, Surj
from alphafe.solutions import parse_solution, verify

from .seedlib import load_seeds, seed_problem

POOL = [T.parse(t) for t in [
    "0", "1", "-1", "2", "x", "y", "-x", "-y", "x+y", "x-y", "y-x", "f(x)", "f(y)", "f(0)", "f(1)",
    "-f(x)", "-f(y)", "x+f(y)", "y-f(x)", "x/2", "(x+y)/2", "2x", "x+1", "y-1", "xy", "f(f(x))", "a", "f(a)", "x^2",
]]
GROUND = [T.parse(t) for t in ["0", "1", "f(0)", "f(1)", "f(0) - 1", "f(-1)", "a", "f(1) - f(0)"]]


def random_move(rng, state):
    n_rows = len(state.current.rows)
    target = "P" if rng.random() < 0.5 or n_rows == 0 else rng.randrange(n_rows)
    roll = rng.random()
    if roll < 0.55:
        names = rng.sample(["x", "y", "z"], rng.choice([1, 1, 2]))
        return Subst(target, tuple((n, rng.choice(POOL)) for n in names))
    options = [
        Split(target), SplitNZ(rng.choice(GROUND)), Inj(), Surj(), Cancel(), Pre(rng.choice(GROUND)),
        Onto(target, rng.choice("xy")), Cauchy(), Quadratic(), Conclude(), Divide(target, rng.choice(GROUND)),
    ]
    return rng.choice(options)


def instantiate(solution_text, rng):
    """Pick random values for the parameters of an expected solution."""
    expr = parse_solution(solution_text)
    values = {a: Poly.const(Fraction(rng.randint(-3, 3), rng.randint(1, 2))) for a in expr.top_atoms() if a[0] == "c"}
    return expr.replace_atoms(values)


def walk(problem, expr, rng, steps):
    state = initial_state(problem)
    check_state(state, expr, rng)
    accepted = 0
    for _ in range(steps):
        if state.solved:
            break
        try:
            state = apply(state, random_move(rng, state))
        except Reject:
            continue
        accepted += 1
        check_state(state, expr, rng)
    return accepted


CASES = [(rec, sol) for rec in load_seeds() for sol in rec["solutions"]]


@pytest.mark.parametrize("record, solution", CASES, ids=[f"{r['id']}:{s}" for r, s in CASES])
def test_random_moves_never_contradict_a_known_solution(record, solution):
    problem = seed_problem(record)
    rng = random.Random(zlib.crc32(f"{record['id']}:{solution}".encode()))
    for _ in range(3):
        expr = instantiate(solution, rng)
        assert verify(problem.poly, expr)
        walk(problem, expr, rng, steps=40)


def test_the_fuzzer_exercises_real_moves():
    """Guard against a fuzzer that silently accepts nothing."""
    rng = random.Random(1)
    total = 0
    for record, solution in CASES[:12]:
        total += walk(seed_problem(record), instantiate(solution, rng), rng, steps=40)
    assert total > 60


def test_modelcheck_detects_a_planted_unsound_fact():
    """If we force a false identity into a branch, the model check notices."""
    problem = seed_problem(load_seeds()[0])           # f(x+y) = f(x) + y, solved by x + c
    state = initial_state(problem)
    state.current.rows.append(parse_poly("f(x) - 2x"))  # false for f(x) = x + 1
    with pytest.raises(Unsound):
        check_state(state, parse_poly("x + 1"), random.Random(0))


def test_modelcheck_detects_a_lost_solution():
    from alphafe.checker import State
    problem = seed_problem(load_seeds()[0])
    empty = State(problem, (), (), ())                # "solved, no solutions"
    with pytest.raises(Unsound):
        check_state(empty, parse_poly("x + 1"), random.Random(0))
