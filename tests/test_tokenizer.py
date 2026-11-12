import random

import pytest

from alphafe import terms as T
from alphafe.checker import Problem, Reject, apply, initial_state
from alphafe.env import start, step
from alphafe.generate import generate
from alphafe.moves import Onto, Pre, Split, SplitNZ, Subst, parse_move
from alphafe.tokenizer import (
    EOS, MAX_MOVE_TOKENS, MAX_STATE_TOKENS, TOKEN_ID, VOCAB, MoveGrammar, decode_move, encode_move, encode_state,
    sample_subterm_move, sample_uniform,
)


def state_of(equation, domain="R", moves=()):
    state = initial_state(Problem.parse(equation, domain))
    for text in moves:
        state = apply(state, parse_move(text))
    return state


def words(view):
    return [VOCAB[i] for i in view.tokens]


def test_vocabulary_is_consistent():
    assert len(set(VOCAB)) == len(VOCAB)
    assert all(VOCAB[i] == tok for tok, i in TOKEN_ID.items())


def test_state_encoding_shows_the_right_things():
    state = state_of("f(x + f(y)) = f(x) + y", "Q", ["inj", "sub P: x:=0"])
    toks = words(encode_state(state))
    assert toks[:3] == ["<bos>", "DOM_Q", "SOLVE"]
    assert "INJ" in toks and "P" in toks and "R1" in toks
    # f(f(y)) = y + f(0) exists for x and for y, but is shown once
    view = encode_state(state)
    assert len(view.row_index) < len(state.current.rows)


def test_goal_conditioned_encoding():
    state = state_of("f(x+y) = f(x) + y")
    goal = state.current.rows[0]
    toks = words(encode_state(state, goal=goal))
    assert toks[2] == "GOAL" and "SOLVE" not in toks


def test_state_encoding_is_bounded():
    encoded = 0
    for item in generate(1, 30)[4]:
        state, _ = start(item.problem())
        if state.solved:                # the routine substitutions finished it: there is no state to encode
            continue
        view = encode_state(state)
        encoded += 1
        assert len(view.tokens) <= MAX_STATE_TOKENS + 120
        assert all(0 <= i < len(VOCAB) for i in view.tokens)
    assert encoded >= 10


MOVES = [
    "sub P: x:=0", "sub P: x:=0, y:=f(y)", "sub P: y:=x - f(x)", "sub P: x:=(x + y)/2, y:=-1", "sub R1: y:=x^2",
    "splitnz f(0)", "splitnz f(1) - 1",
]


@pytest.mark.parametrize("text", MOVES)
def test_move_round_trip(text):
    state = state_of("f(x + f(y)) = f(x) + y", "Q", ["sub P: x:=0"])
    view = encode_state(state)
    move = parse_move(text)
    ids = encode_move(move, view)
    assert ids is not None and ids[-1] == EOS
    back = decode_move(ids, view)
    assert encode_move(back, view) == ids


def test_split_pre_onto_round_trip():
    state = state_of("f(x)f(y) = f(x+y) + xy", "R", ["sub P: x:=0, y:=0"])
    view = encode_state(state)
    assert view.splittable == ["R1"]
    assert decode_move(encode_move(Split(0), view), view) == Split(0)
    state = state_of("f(x + f(y)) = f(x) + y", "R", ["sub P: x:=0", "surj"])
    view = encode_state(state)
    assert decode_move(encode_move(Pre(T.num(0)), view), view) == Pre(T.num(0))
    assert decode_move(encode_move(Onto(0, "y"), view), view) == Onto(0, "y")


def test_unencodable_moves_return_none():
    view = encode_state(state_of("f(x+y) = f(x) + y"))
    assert encode_move(parse_move("conclude"), view) is None             # free move
    assert encode_move(parse_move("sub [f(x) = x]: x:=0"), view) is None  # quoted target
    assert encode_move(parse_move("sub R9: x:=0"), view) is None          # no such row
    assert encode_move(parse_move("sub P: x:=1000"), view) is None        # number outside the vocabulary


def test_grammar_offers_only_what_exists():
    plain = MoveGrammar(encode_state(state_of("f(x+y) = f(x) + f(y)")))
    assert set(plain.allowed_tokens()) == {"SUB", "SPLITNZ"}              # nothing to split, not surjective
    split = MoveGrammar(encode_state(state_of("f(x)f(y) = f(x+y) + xy", "R", ["sub P: x:=0, y:=0"])))
    assert "SPLIT" in split.allowed_tokens()
    surj = MoveGrammar(encode_state(state_of("f(x + f(y)) = f(x) + y", "R", ["surj"])))
    assert {"PRE", "ONTO"} <= set(surj.allowed_tokens())


def test_grammar_rejects_disallowed_tokens():
    grammar = MoveGrammar(encode_state(state_of("f(x+y) = f(x) + y")))
    with pytest.raises(ValueError):
        grammar.advance(TOKEN_ID["PRE"])
    grammar.advance(TOKEN_ID["SUB"])
    assert grammar.allowed_tokens() == ["P", "R1"]
    grammar.advance(TOKEN_ID["P"])
    assert grammar.allowed_tokens() == ["x", "y"]                         # must bind something before <eos>
    grammar.advance(TOKEN_ID["y"])
    grammar.advance(TOKEN_ID["0"])
    assert grammar.allowed_tokens() == ["<eos>"]                          # y was the last variable
    grammar.advance(EOS)
    assert grammar.done


def test_every_grammar_sample_is_a_well_formed_move():
    """Property: whatever the uniform policy writes, it decodes, re-encodes and is bounded in length."""
    rng = random.Random(0)
    states = [
        state_of("f(x+y) = f(x) + y"),
        state_of("f(x)f(y) = f(x+y) + xy", "R", ["sub P: x:=0, y:=0"]),
        state_of("f(x + f(y)) = f(x) + y", "R", ["sub P: x:=0", "surj", "pre 0"]),
    ]
    accepted = 0
    for state in states:
        view = encode_state(state)
        for _ in range(400):
            ids, logp = sample_uniform(view, rng)
            assert ids[-1] == EOS and len(ids) <= MAX_MOVE_TOKENS and logp < 0
            move = decode_move(ids, view)
            assert isinstance(move, (Subst, Split, SplitNZ, Pre, Onto))
            try:
                step(state, move)
                accepted += 1
            except Reject:
                pass
    assert accepted > 100          # and a fair share of them are legal moves


def test_subterm_exploration_proposes_expressions_from_the_state():
    """Self-play exploration can suggest 'substitute something already on the page', e.g. y := f(y)."""
    from alphafe import terms as T
    from alphafe.moves import show_move

    state = state_of("f(x + f(y)) = f(x) + y", "Q")
    view = encode_state(state)
    shown = {T.show(t) for t in view.subterms}
    assert {"f(y)", "f(x)", "f(y) + x"} <= shown
    rng = random.Random(0)
    moves = set()
    for _ in range(1500):
        sample = sample_subterm_move(view, rng)
        assert sample is not None
        ids, logp = sample
        assert ids[-1] == EOS and logp < 0
        moves.add(show_move(decode_move(ids, view)))
    assert "sub P: y:=f(y)" in moves and "sub P: x:=-f(y)" in moves
    assert view.subterms == encode_state(state).subterms          # same order every time
    assert all(m.startswith("sub ") for m in moves)


def test_problems_in_other_letters_are_renamed_for_the_network(plain_environment):
    """The checker accepts x y z t u v w; the network vocabulary has x, y, z. (This used to raise KeyError.)"""
    import random

    import pytest

    from alphafe.bench import BenchProblem
    from alphafe.eval import run_policy
    from alphafe.search import UniformProposer

    problem = Problem.parse("f(x+w) = f(x) + w")
    with pytest.raises(ValueError, match="x, y, z only"):
        encode_state(start(problem)[0])
    renamed, names = problem.standard_names()
    assert names == {"w": "y"} and renamed.equation == "f(x + y) = f(x) + y"       # x keeps its name
    assert encode_state(start(renamed)[0]).tokens
    three, names = Problem.parse("f(t+u+v) = f(t) + u + v").standard_names()
    assert names == {"t": "x", "u": "y", "v": "z"} and sorted(three.poly.variables()) == ["x", "y", "z"]
    same, names = Problem.parse("f(x+y) = f(x) + y").standard_names()
    assert names == {} and same.equation == "f(x+y) = f(x) + y"
    # The policy searches rename by themselves, so a benchmark row in u, v is scored and not a crash.
    bench = BenchProblem("uv", Problem.parse("f(u + v) = f(u) + v"), None)
    rows = run_policy([bench], UniformProposer(random.Random(0)), "search", 64)
    assert rows[0].solved and rows[0].equation == "f(u + v) = f(u) + v"


def test_a_split_is_offered_only_where_the_checker_accepts_one():
    """Every fact the grammar offers for a case split is one the checker splits; facts it refuses are among the rest."""
    rng = random.Random(5)
    offered = refused = 0
    for item in generate(11, 30)[4][:30]:
        try:
            state, _ = start(item.problem())
        except Reject:
            continue
        for _ in range(6):
            if state.solved:
                break
            view = encode_state(state)
            for label, index in view.row_index.items():
                row = state.current.rows[index]
                if row.variables():
                    continue
                try:
                    apply(state, Split(index))
                    accepted = True
                except Reject as err:
                    accepted = "too many" in str(err)          # room for the cases is not the grammar's business
                if label in view.splittable:
                    assert accepted
                    offered += 1
                elif not accepted:
                    refused += 1
            try:
                state, _ = step(state, decode_move(sample_uniform(view, rng)[0], view))
            except Reject:
                pass
    assert offered and refused


def test_argument_substitutions_solve_an_argument_of_f_for_a_variable():
    from alphafe.algebra import poly_str
    from alphafe.tokenizer import argument_substitutions

    poly = Problem.parse("f(f(x) + y) = f(x^2 - y) + 4y f(x)", "R").poly
    found = {(name, poly_str(value)) for name, value in argument_substitutions(poly)}
    assert ("y", "-f(x)") in found                            # f(x) + y vanishes
    assert ("y", "x^2") in found                              # x^2 - y vanishes
    assert ("y", "x^2/2 - f(x)/2") in found                   # the two arguments become equal
    assert ("y", "y - f(x)") in found                         # the first argument becomes y alone
    assert ("x", "y") in found and ("x", "0") in found        # the inner argument x
    assert not any(name == "x" and "f" in text for name, text in found)   # nothing is solved through f or a square
    # One variable, one argument: the only thing to do is to make it vanish.
    assert [(name, poly_str(value)) for name, value in argument_substitutions(Problem.parse("f(x) = x", "R").poly)] == [("x", "0")]


def test_argument_moves_are_well_formed_and_some_are_accepted(plain_environment):
    from alphafe.tokenizer import sample_argument_move

    rng = random.Random(3)
    state, _ = start(Problem.parse("f(x + f(y)) = f(x) + y", "R"))
    state = apply(state, parse_move("surj")) if "surjective" not in state.current.props else state
    view = encode_state(state)
    kinds, accepted = set(), 0
    for _ in range(200):
        sample = sample_argument_move(view, rng)
        if sample is None:
            continue
        move = decode_move(sample[0], view)
        assert encode_move(move, view) == sample[0] and sample[1] < 0
        kinds.add(type(move).__name__)
        try:
            apply(state, move)
            accepted += 1
        except Reject:
            pass
    assert kinds == {"Subst", "Pre"} and accepted
