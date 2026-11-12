"""Known proofs for disguised problems (``generate.disguise``).

A disguised problem is a plain one behind one or more changes of variables.
Its proof is known without any search: undo the changes, one proposed move
each, and then put into the plain equation, which is now a derived identity,
the opening substitutions that the environment only ever makes into the
original equation. Whatever of that is not needed is dropped, and the result
counts only if replaying it through the environment solves the problem.

Such proofs have several proposed moves in a row, which self-play on
randomly built equations almost never finds. Nothing here uses a benchmark
or the brute-force baseline.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Optional

from . import terms as T
from .checker import Problem, Reject, State, apply
from .env import _opening_moves, start, step
from .moves import EqRef, Move, Subst, parse_move


def solves(problem: Problem, moves: list) -> bool:
    """Do these proposed moves, each followed by the environment's own, solve the problem with none left over?"""
    try:
        state, _ = start(problem)
        for move in moves:
            if state.solved:
                return False
            state, _ = step(state, move)
    except Reject:
        return False
    return state.solved


def planted_proof(item) -> Optional[list[Move]]:
    """The proposed moves of the known proof of a disguised problem, or None.

    None if the problem is not a disguised one, if the environment solves it
    without any proposed move (there is nothing to learn from it then), or if
    the known proof does not go through.
    """
    if not item.plan:
        return None
    problem = item.problem()
    moves: list[Move] = []
    try:
        state, _ = start(problem)
        if state.solved:
            return None
        for text in item.plan:
            move = parse_move(text)
            state, _ = step(state, move)
            moves.append(move)
            if state.solved:
                break
    except Reject:
        return None
    if not state.solved:
        # The plain equation is known now, but as a derived identity: the environment made its
        # opening substitutions into the disguised equation. Make them into the plain one.
        target = EqRef(*T.parse_equation(item.plain))
        for opening in _opening_moves(Problem.parse(item.plain, item.domain)):
            move = Subst(target, opening.bindings)
            try:
                state, _ = step(state, move)
            except Reject:
                continue
            moves.append(move)
            if state.solved:
                break
    if not state.solved:
        return None
    index = 0
    while index < len(moves) and len(moves) > 1:
        shorter = moves[:index] + moves[index + 1:]
        if solves(problem, shorter):
            moves = shorter
        else:
            index += 1
    return moves if solves(problem, moves) else None


def written(state: State, move: Move) -> Optional[Move]:
    """``move`` with a row number in place of a quoted identity, which is how the network writes a target.

    The row is one that gives the same state as the quoted identity does.
    None if no row does (the identity is known only as a consequence of
    several rows).
    """
    target = getattr(move, "target", None)
    if not isinstance(target, EqRef):
        return move
    try:
        wanted = apply(state, move).key()
    except Reject:
        return None
    names = {name for name, _ in move.bindings} if isinstance(move, Subst) else set()
    for index, row in enumerate(state.current.rows):
        if not names <= row.variables():
            continue
        candidate = replace(move, target=index)
        try:
            if apply(state, candidate).key() == wanted:
                return candidate
        except Reject:
            continue
    return None
