"""Known proofs of disguised problems (alphafe/planted.py) are real proofs, and their examples replay."""

import random

from alphafe.checker import check
from alphafe.env import start, step
from alphafe.generate import disguise, generate
from alphafe.moves import EqRef, show_move
from alphafe.planted import planted_proof, solves, written
from alphafe.tokenizer import decode_move, encode_move, encode_state
from alphafe.train import planted_examples

DATA = generate(11, 30)
ITEMS = [item for items in DATA.values() for item in items]


def _hidden(limit: int) -> list:
    out = []
    for index, item in enumerate(ITEMS):
        hidden = disguise(item, random.Random(f"t:{item.key}"), 1 + index % 2)
        if hidden is not None and planted_proof(hidden) is not None:
            out.append(hidden)
            if len(out) == limit:
                break
    return out


HIDDEN = _hidden(8)


def test_some_disguised_problems_have_a_known_proof_of_several_moves():
    assert len(HIDDEN) == 8
    assert any(len(planted_proof(item)) >= 3 for item in HIDDEN)


def test_a_known_proof_is_a_complete_proof_and_no_move_of_it_can_be_dropped():
    for item in HIDDEN:
        problem = item.problem()
        proof = planted_proof(item)
        assert len(proof) >= 2 or not isinstance(proof[0].target, EqRef)
        # Replayed through the environment, then checked from scratch by the checker alone.
        state, moves = start(problem)
        assert not state.solved
        for move in proof:
            state, applied = step(state, move)
            moves = moves + applied
        assert state.solved and check(problem, moves).solved, item.equation
        if len(proof) > 1:
            for index in range(len(proof)):
                assert not solves(problem, proof[:index] + proof[index + 1:]), (item.equation, index)


def test_the_environment_alone_does_not_solve_a_problem_with_a_known_proof():
    for item in HIDDEN:
        assert not start(item.problem())[0].solved


def test_examples_are_the_moves_of_the_known_proof_as_the_network_writes_them():
    seen = 0
    for item in HIDDEN:
        examples = planted_examples(item)
        state, _ = start(item.problem())
        direct = []
        for move in planted_proof(item):
            view = encode_state(state)
            shown = written(state, move)
            if shown is not None:
                # A row number in place of the quoted identity, and the same state after the move.
                assert not isinstance(shown.target, EqRef)
                assert step(state, shown)[0].key() == step(state, move)[0].key()
                ids = encode_move(shown, view)
                if ids is not None:                       # None: the row is not among those shown
                    # Compared as text: -1 is one number in an opening move and a negated 1 when read back.
                    assert show_move(decode_move(ids, view)) == show_move(shown)
                    direct.append((tuple(view.tokens), tuple(ids)))
            state, _ = step(state, move)
        # The proof's own steps come first, in order; the mirror image, if any, follows.
        assert examples[:len(direct)] == direct
        assert len(examples) in (len(direct), 2 * len(direct))
        seen += len(direct)
    assert seen >= 8


def test_a_plain_problem_has_no_known_proof():
    assert planted_proof(ITEMS[0]) is None and planted_examples(ITEMS[0]) == []
