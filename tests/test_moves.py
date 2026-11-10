import pytest

from alphafe import terms as T
from alphafe.moves import (
    Cancel, Cauchy, Conclude, Divide, EqRef, Inj, Onto, Pre, Split, SplitNZ, Subst, Surj,
    parse_move, parse_proof, show_move,
)

P = T.parse

EXAMPLES = [
    ("sub P: x:=0, y:=f(y)", Subst("P", (("x", P("0")), ("y", P("f(y)"))))),
    ("sub R2: x:=y", Subst(1, (("x", P("y")),))),
    ("sub [f(f(x)) = x]: x:=y + 1", Subst(EqRef(P("f(f(x))"), P("x")), (("x", P("y+1")),))),
    ("split R1", Split(0)),
    ("split R1 by f(0), f(0) - 1", Split(0, (P("f(0)"), P("f(0)-1")))),
    ("splitnz f(0)", SplitNZ(P("f(0)"))),
    ("div R3 by f(0)", Divide(2, P("f(0)"))),
    ("inj", Inj()),
    ("surj R1", Surj(0)),
    ("cancel [f(x) = f(y)]", Cancel(EqRef(P("f(x)"), P("f(y)")))),
    ("pre 0", Pre(P("0"))),
    ("onto R2: y", Onto(1, "y")),
    ("cauchy", Cauchy()),
    ("conclude", Conclude()),
]


@pytest.mark.parametrize("text, move", EXAMPLES)
def test_parse_and_show(text, move):
    assert parse_move(text) == move
    assert parse_move(show_move(move)) == move


@pytest.mark.parametrize("bad", ["", "sub P x:=0", "sub P:", "sub Q: x:=0", "sub P: a:=0", "jump", "div R1", "onto R1", "split R0"])
def test_parse_rejects(bad):
    with pytest.raises(T.ParseError):
        parse_move(bad)


def test_parse_proof_skips_comments_and_blanks():
    proof = parse_proof("""
        # a comment
        sub P: x:=0    # trailing comment

        conclude
    """)
    assert proof == [Subst("P", (("x", P("0")),)), Conclude()]
