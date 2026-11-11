"""The proof moves and their text format.

A proof is a list of moves. This module only defines what a move *looks like*
(the data and the plain-text syntax); what a move *means*, and when it is
legal, is decided by ``alphafe.checker``.

Text format, one move per line (``#`` starts a comment)::

    sub P: x:=0, y:=f(y)        substitute into the original equation
    sub R2: x:=y                substitute into the 2nd current identity
    sub [f(f(x)) = x]: x:=y+1   substitute into a quoted known identity
    split R1                    case split on a factorised fact about constants
    split R1 by f(0), f(0)-1    ... with the factors spelled out
    splitnz f(0)                case split: f(0) = 0  or  f(0) != 0
    div R3 by f(0)              divide an identity by a proven-nonzero constant
    inj                         establish injectivity
    surj                        establish surjectivity
    cancel R2                   cancel f from f(A) = f(B) using injectivity
    pre 0                       pick a with f(a) = 0 using surjectivity
    onto R2: y                  f is surjective and y only occurs as f(y):
                                replace f(y) by y
    cauchy                      additive (up to a polynomial) over Q implies polynomial
    quadratic                   f(x+y) + f(x-y) = 2f(x) + 2f(y) over Q implies f(x) = f(1)x^2
    conclude                    read off f(x) = ... and pin down the constants

Where a target (``P``, ``R2`` or ``[...]``) is optional and omitted, the
checker uses the first identity the move applies to.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Union

from . import terms as T


@dataclass(frozen=True)
class EqRef:
    """A target given by quoting an identity; the checker must confirm it is known."""

    lhs: T.Term
    rhs: T.Term


# 'P' is the original equation, an int is a 0-based index into the current
# identities (shown 1-based as R1, R2, ...), an EqRef quotes an identity.
Target = Union[str, int, EqRef]


@dataclass(frozen=True)
class Subst:
    target: Target
    bindings: tuple  # ((variable name, Term), ...)


@dataclass(frozen=True)
class Split:
    target: Target
    factors: tuple = ()  # optional explicit factor Terms


@dataclass(frozen=True)
class SplitNZ:
    term: T.Term


@dataclass(frozen=True)
class Divide:
    target: Target
    term: T.Term


@dataclass(frozen=True)
class Inj:
    target: Optional[Target] = None


@dataclass(frozen=True)
class Surj:
    target: Optional[Target] = None


@dataclass(frozen=True)
class Cancel:
    target: Optional[Target] = None


@dataclass(frozen=True)
class Pre:
    term: T.Term


@dataclass(frozen=True)
class Onto:
    target: Target
    var: str


@dataclass(frozen=True)
class Cauchy:
    target: Optional[Target] = None


@dataclass(frozen=True)
class Quadratic:
    target: Optional[Target] = None


@dataclass(frozen=True)
class Conclude:
    target: Optional[Target] = None


Move = Union[Subst, Split, SplitNZ, Divide, Inj, Surj, Cancel, Pre, Onto, Cauchy, Quadratic, Conclude]

_SIMPLE = {"inj": Inj, "surj": Surj, "cancel": Cancel, "cauchy": Cauchy, "quadratic": Quadratic, "conclude": Conclude}
_SIMPLE_NAMES = {cls: name for name, cls in _SIMPLE.items()}


# ---------------------------------------------------------------------------
# Printing
# ---------------------------------------------------------------------------

def show_target(target: Target) -> str:
    if target == "P":
        return "P"
    if isinstance(target, int):
        return f"R{target + 1}"
    if isinstance(target, EqRef):
        return f"[{T.show(target.lhs)} = {T.show(target.rhs)}]"
    raise TypeError(f"not a target: {target!r}")


def show_move(move: Move) -> str:
    """Print a move in the text format (``parse_move`` reads it back)."""
    if isinstance(move, Subst):
        bindings = ", ".join(f"{name}:={T.show(term)}" for name, term in move.bindings)
        return f"sub {show_target(move.target)}: {bindings}"
    if isinstance(move, Split):
        text = f"split {show_target(move.target)}"
        if move.factors:
            text += " by " + ", ".join(T.show(t) for t in move.factors)
        return text
    if isinstance(move, SplitNZ):
        return f"splitnz {T.show(move.term)}"
    if isinstance(move, Divide):
        return f"div {show_target(move.target)} by {T.show(move.term)}"
    if isinstance(move, Pre):
        return f"pre {T.show(move.term)}"
    if isinstance(move, Onto):
        return f"onto {show_target(move.target)}: {move.var}"
    name = _SIMPLE_NAMES.get(type(move))
    if name is None:
        raise TypeError(f"not a move: {move!r}")
    return name if move.target is None else f"{name} {show_target(move.target)}"


def show_proof(proof) -> str:
    return "\n".join(show_move(m) for m in proof)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def parse_target(text: str) -> Target:
    text = text.strip()
    if text == "P":
        return "P"
    if text.startswith("R") and text[1:].isdigit() and int(text[1:]) >= 1:
        return int(text[1:]) - 1
    if text.startswith("[") and text.endswith("]"):
        lhs, rhs = T.parse_equation(text[1:-1])
        return EqRef(lhs, rhs)
    raise T.ParseError(f"not a target (expected P, R<n> or [equation]): {text!r}")


def _split_commas(text: str) -> list[str]:
    """Split on commas that are not inside brackets."""
    parts, depth, current = [], 0, []
    for ch in text:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(ch)
    parts.append("".join(current))
    return [p.strip() for p in parts if p.strip()]


def parse_move(text: str) -> Move:
    text = text.strip()
    if not text:
        raise T.ParseError("empty move")
    head, _, rest = text.partition(" ")
    rest = rest.strip()
    if head == "sub":
        target_text, sep, bindings_text = rest.partition(":")
        # the first ':' might belong to ':=' when the target is followed directly by bindings
        if not sep or bindings_text.startswith("="):
            raise T.ParseError("expected 'sub <target>: x:=term, ...'")
        bindings = []
        for part in _split_commas(bindings_text):
            name, sep, term_text = part.partition(":=")
            name = name.strip()
            if not sep or name not in T.VAR_NAMES or len(name) != 1:
                raise T.ParseError(f"bad binding {part!r}")
            bindings.append((name, T.parse(term_text)))
        if not bindings:
            raise T.ParseError("a substitution needs at least one binding")
        return Subst(parse_target(target_text), tuple(bindings))
    if head == "split":
        target_text, sep, factors_text = rest.partition(" by ")
        factors = tuple(T.parse(p) for p in _split_commas(factors_text)) if sep else ()
        return Split(parse_target(target_text), factors)
    if head == "splitnz":
        return SplitNZ(T.parse(rest))
    if head == "div":
        target_text, sep, term_text = rest.partition(" by ")
        if not sep:
            raise T.ParseError("expected 'div <target> by <term>'")
        return Divide(parse_target(target_text), T.parse(term_text))
    if head == "pre":
        return Pre(T.parse(rest))
    if head == "onto":
        target_text, sep, var = rest.rpartition(":")
        var = var.strip()
        if not sep or len(var) != 1 or var not in T.VAR_NAMES:
            raise T.ParseError("expected 'onto <target>: <variable>'")
        return Onto(parse_target(target_text), var)
    if head in _SIMPLE:
        return _SIMPLE[head](parse_target(rest) if rest else None)
    raise T.ParseError(f"unknown move {head!r}")


def parse_proof(text: str) -> list[Move]:
    """Parse a whole proof: one move per line, blank lines and # comments ignored."""
    moves = []
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if line:
            try:
                moves.append(parse_move(line))
            except T.ParseError as err:
                raise T.ParseError(f"line {number}: {line!r}: {err}") from None
    return moves
