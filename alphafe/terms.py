"""Expression trees for functional equations, with a parser and two printers.

A *term* is built from

* rational numbers                       ``Num``
* universally quantified variables       ``Var``   (x, y, z, t, u, v, w)
* named constants                        ``Sym``   (a, b, c, ... : witnesses in
                                                    proofs, parameters in answers)
* ``+``, ``-``, ``*``, integer powers    ``Add, Sub, Mul, Neg, Pow``
* the unknown function applied to a term ``App``   written ``f(...)``

Two concrete syntaxes share this one tree type:

* infix text, for people:  ``f(x + f(y)) = f(x) + y``     (``parse`` / ``show``)
* prefix tokens, for the network: ``= f + x f y + f x y`` (``to_prefix`` / ``from_prefix``)

Nothing here decides whether two terms are *equal*; that is the job of
``alphafe.algebra``, which turns terms into canonical polynomials.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

VAR_NAMES = "xyztuvw"
CONST_NAMES = "abcdeghkmnpqrs"  # every other lowercase letter except f


class Term:
    """Base class for expression-tree nodes (all nodes are immutable)."""

    __slots__ = ()

    def __str__(self) -> str:
        return show(self)


@dataclass(frozen=True, slots=True)
class Num(Term):
    value: Fraction


@dataclass(frozen=True, slots=True)
class Var(Term):
    name: str


@dataclass(frozen=True, slots=True)
class Sym(Term):
    name: str


@dataclass(frozen=True, slots=True)
class Add(Term):
    left: Term
    right: Term


@dataclass(frozen=True, slots=True)
class Sub(Term):
    left: Term
    right: Term


@dataclass(frozen=True, slots=True)
class Mul(Term):
    left: Term
    right: Term


@dataclass(frozen=True, slots=True)
class Neg(Term):
    arg: Term


@dataclass(frozen=True, slots=True)
class Pow(Term):
    base: Term
    exp: int


@dataclass(frozen=True, slots=True)
class App(Term):
    arg: Term


def num(value) -> Num:
    return Num(Fraction(value))


class ParseError(ValueError):
    """Raised when text (or a prefix token list) is not a well-formed term."""


# ---------------------------------------------------------------------------
# Infix parser
# ---------------------------------------------------------------------------

def _tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch.isspace():
            i += 1
        elif ch.isdigit():
            j = i
            while j < n and text[j].isdigit():
                j += 1
            tokens.append(text[i:j])
            i = j
        elif ch.isalpha():
            if not ch.islower() or not ch.isascii():
                raise ParseError(f"unexpected character {ch!r}")
            tokens.append(ch)
            i += 1
        elif ch in "+-*/^()=":
            tokens.append(ch)
            i += 1
        else:
            raise ParseError(f"unexpected character {ch!r}")
    return tokens


class _Parser:
    """Recursive-descent parser.

    Grammar (``INT`` is an unsigned integer literal)::

        expr   := term (('+' | '-') term)*
        term   := unary (('*' | <juxtaposition>) unary | '/' INT)*
        unary  := '-' unary | power
        power  := base ('^' INT)?
        base   := INT | letter | 'f' '(' expr ')' | '(' expr ')'

    Division is only allowed by an integer literal: it is how rational
    constants are written (``x/2``, ``3/4``). Dividing by an expression is out
    of scope for version 1.
    """

    def __init__(self, tokens: list[str]):
        self.toks = tokens
        self.pos = 0

    def peek(self) -> str | None:
        return self.toks[self.pos] if self.pos < len(self.toks) else None

    def take(self) -> str:
        tok = self.peek()
        if tok is None:
            raise ParseError("unexpected end of input")
        self.pos += 1
        return tok

    def expect(self, tok: str) -> None:
        got = self.take()
        if got != tok:
            raise ParseError(f"expected {tok!r} but found {got!r}")

    def expr(self) -> Term:
        left = self.term()
        while self.peek() in ("+", "-"):
            op = self.take()
            right = self.term()
            left = Add(left, right) if op == "+" else Sub(left, right)
        return left

    def _starts_factor(self) -> bool:
        tok = self.peek()
        return tok is not None and (tok == "(" or tok.isalpha())

    def term(self) -> Term:
        left = self.unary()
        while True:
            tok = self.peek()
            if tok == "*":
                self.take()
                left = Mul(left, self.unary())
            elif tok == "/":
                self.take()
                den = self.take()
                if not den.isdigit():
                    raise ParseError("division is only allowed by an integer literal")
                if int(den) == 0:
                    raise ParseError("division by zero")
                if isinstance(left, Num):
                    left = Num(left.value / int(den))
                else:
                    left = Mul(left, Num(Fraction(1, int(den))))
            elif self._starts_factor():
                left = Mul(left, self.power())
            else:
                return left

    def unary(self) -> Term:
        if self.peek() == "-":
            self.take()
            return Neg(self.unary())
        return self.power()

    def power(self) -> Term:
        base = self.base()
        if self.peek() == "^":
            self.take()
            exp = self.take()
            if not exp.isdigit():
                raise ParseError("exponent must be a non-negative integer literal")
            return Pow(base, int(exp))
        return base

    def base(self) -> Term:
        tok = self.take()
        if tok.isdigit():
            return Num(Fraction(int(tok)))
        if tok == "(":
            inner = self.expr()
            self.expect(")")
            return inner
        if tok == "f":
            if self.peek() != "(":
                raise ParseError("'f' must be applied: write f(...)")
            self.take()
            inner = self.expr()
            self.expect(")")
            return App(inner)
        if tok in VAR_NAMES:
            return Var(tok)
        if tok in CONST_NAMES:
            return Sym(tok)
        raise ParseError(f"unexpected token {tok!r}")


def parse(text: str) -> Term:
    """Parse infix text such as ``2x*f(y) - f(x + 1)^2`` into a term."""
    parser = _Parser(_tokenize(text))
    result = parser.expr()
    if parser.peek() is not None:
        raise ParseError(f"unexpected token {parser.peek()!r}")
    return result


def parse_equation(text: str) -> tuple[Term, Term]:
    """Parse ``lhs = rhs`` into a pair of terms."""
    if text.count("=") != 1:
        raise ParseError("an equation needs exactly one '='")
    left, right = text.split("=")
    return parse(left), parse(right)


# ---------------------------------------------------------------------------
# Infix printer
# ---------------------------------------------------------------------------

# Precedence levels: 1 sum, 2 product, 3 unary minus, 4 power, 5 atom.

def _prec(term: Term) -> int:
    if isinstance(term, (Add, Sub)):
        return 1
    if isinstance(term, Mul):
        return 2
    if isinstance(term, Neg):
        return 3
    if isinstance(term, Pow):
        return 4
    if isinstance(term, Num):
        if term.value < 0:
            return 3
        if term.value.denominator != 1:
            return 2
    return 5


def _wrap(term: Term, min_prec: int) -> str:
    text = show(term)
    return f"({text})" if _prec(term) < min_prec else text


def show(term: Term) -> str:
    """Print a term as infix text that ``parse`` reads back to an equal term."""
    if isinstance(term, Num):
        v = term.value
        return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"
    if isinstance(term, (Var, Sym)):
        return term.name
    if isinstance(term, App):
        return f"f({show(term.arg)})"
    if isinstance(term, Add):
        # a + (b - c) may drop the brackets: addition is associative
        return f"{_wrap(term.left, 1)} + {_wrap(term.right, 1)}"
    if isinstance(term, Sub):
        return f"{_wrap(term.left, 1)} - {_wrap(term.right, 2)}"
    if isinstance(term, Neg):
        return f"-{_wrap(term.arg, 2)}"
    if isinstance(term, Pow):
        return f"{_wrap(term.base, 5)}^{term.exp}"
    if isinstance(term, Mul):
        left, right = term.left, term.right
        # x * (1/n) prints as x/n
        if isinstance(right, Num) and right.value.numerator == 1 and right.value.denominator != 1:
            return f"{_wrap(left, 2)}/{right.value.denominator}"
        ls = _wrap(left, 2)
        if isinstance(left, Num) and left.value.denominator != 1 and left.value > 0:
            ls = f"({ls})"
        # x(yz) may drop the brackets: multiplication is associative
        rs = _wrap(right, 2 if isinstance(right, Mul) else 4)
        if rs.startswith("-"):
            rs = f"({rs})"  # x(-2y), never x-2y
        # Juxtapose (2x, xf(y), f(x)f(y)) unless the right factor starts with a
        # digit, in which case juxtaposition would glue two numbers together.
        if rs[0].isdigit():
            return f"{ls}*{rs}"
        return f"{ls}{rs}"
    raise TypeError(f"not a term: {term!r}")


def show_equation(lhs: Term, rhs: Term) -> str:
    return f"{show(lhs)} = {show(rhs)}"


# ---------------------------------------------------------------------------
# Prefix (Polish) notation, used by the tokenizer
# ---------------------------------------------------------------------------

MAX_INT_TOKEN = 20          # integers 0..20 are single tokens
BIG_INT = "N"               # placeholder for any larger integer (lossy)
PREFIX_BINARY = ("+", "-", "*", "^", "/")
PREFIX_UNARY = ("~", "f")


def _int_token(n: int) -> str:
    return str(n) if n <= MAX_INT_TOKEN else BIG_INT


def to_prefix(term: Term) -> list[str]:
    """Serialise a term to prefix tokens.

    ``~`` is unary minus, ``/ p q`` is the rational p/q, ``^ t n`` is a power.
    Prefix notation needs no brackets, which makes grammar-constrained decoding
    simple: the decoder only has to count how many operands are still owed.
    """
    out: list[str] = []
    _prefix(term, out)
    return out


def _prefix(term: Term, out: list[str]) -> None:
    if isinstance(term, Num):
        v = term.value
        if v < 0:
            out.append("~")
            v = -v
        if v.denominator == 1:
            out.append(_int_token(v.numerator))
        else:
            out.extend(["/", _int_token(v.numerator), _int_token(v.denominator)])
    elif isinstance(term, (Var, Sym)):
        out.append(term.name)
    elif isinstance(term, App):
        out.append("f")
        _prefix(term.arg, out)
    elif isinstance(term, Neg):
        out.append("~")
        _prefix(term.arg, out)
    elif isinstance(term, Pow):
        out.append("^")
        _prefix(term.base, out)
        out.append(_int_token(term.exp))
    elif isinstance(term, (Add, Sub, Mul)):
        out.append({Add: "+", Sub: "-", Mul: "*"}[type(term)])
        _prefix(term.left, out)
        _prefix(term.right, out)
    else:
        raise TypeError(f"not a term: {term!r}")


def from_prefix(tokens: list[str]) -> Term:
    """Parse a complete prefix token list back into a term."""
    term, pos = _from_prefix(tokens, 0)
    if pos != len(tokens):
        raise ParseError("trailing tokens after prefix term")
    return term


def _from_prefix(tokens: list[str], pos: int) -> tuple[Term, int]:
    if pos >= len(tokens):
        raise ParseError("unexpected end of prefix term")
    tok = tokens[pos]
    pos += 1
    if tok.isdigit():
        return Num(Fraction(int(tok))), pos
    if tok in VAR_NAMES and len(tok) == 1:
        return Var(tok), pos
    if tok in CONST_NAMES and len(tok) == 1:
        return Sym(tok), pos
    if tok == "f":
        arg, pos = _from_prefix(tokens, pos)
        return App(arg), pos
    if tok == "~":
        arg, pos = _from_prefix(tokens, pos)
        return Neg(arg), pos
    if tok in ("+", "-", "*"):
        left, pos = _from_prefix(tokens, pos)
        right, pos = _from_prefix(tokens, pos)
        return {"+": Add, "-": Sub, "*": Mul}[tok](left, right), pos
    if tok == "^":
        base, pos = _from_prefix(tokens, pos)
        exp, pos = _from_prefix(tokens, pos)
        if not isinstance(exp, Num) or exp.value.denominator != 1 or exp.value < 0:
            raise ParseError("exponent must be a non-negative integer")
        return Pow(base, int(exp.value)), pos
    if tok == "/":
        p, pos = _from_prefix(tokens, pos)
        q, pos = _from_prefix(tokens, pos)
        if not (isinstance(p, Num) and isinstance(q, Num)) or q.value == 0:
            raise ParseError("'/' takes two integer literals with a nonzero denominator")
        return Num(p.value / q.value), pos
    raise ParseError(f"unexpected prefix token {tok!r}")


# ---------------------------------------------------------------------------
# Small structural helpers
# ---------------------------------------------------------------------------

def subterms(term: Term):
    """Yield every node of the tree, parents before children."""
    yield term
    if isinstance(term, (Add, Sub, Mul)):
        yield from subterms(term.left)
        yield from subterms(term.right)
    elif isinstance(term, (Neg, App)):
        yield from subterms(term.arg)
    elif isinstance(term, Pow):
        yield from subterms(term.base)


def term_size(term: Term) -> int:
    """Number of nodes in the tree."""
    return sum(1 for _ in subterms(term))


def nesting_depth(term: Term) -> int:
    """Maximum number of nested applications of f (f(f(x)) has depth 2)."""
    if isinstance(term, App):
        return 1 + nesting_depth(term.arg)
    if isinstance(term, (Add, Sub, Mul)):
        return max(nesting_depth(term.left), nesting_depth(term.right))
    if isinstance(term, Neg):
        return nesting_depth(term.arg)
    if isinstance(term, Pow):
        return nesting_depth(term.base)
    return 0


def max_exponent(term: Term) -> int:
    """The largest exponent in a term, nested powers multiplied: (x^2)^3 counts as 6."""
    if isinstance(term, Pow):
        return term.exp * max(1, max_exponent(term.base))
    if isinstance(term, (Add, Sub, Mul)):
        return max(max_exponent(term.left), max_exponent(term.right))
    if isinstance(term, (Neg, App)):
        return max_exponent(term.arg)
    return 1


def term_vars(term: Term) -> set[str]:
    return {t.name for t in subterms(term) if isinstance(t, Var)}


def term_syms(term: Term) -> set[str]:
    return {t.name for t in subterms(term) if isinstance(t, Sym)}
