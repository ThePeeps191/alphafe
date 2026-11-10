"""Tokenizer: proof states and moves as token sequences, plus the move grammar.

The network reads a proof state as tokens and writes its next move as tokens.
Expressions use prefix notation (see ``terms.to_prefix``). The network only
writes the *creative* moves:

    SUB <target> (<variable> <term>)+ <eos>     substitution
    SPLIT <row> <eos>                           case split on a fact about constants
    SPLITNZ <term> <eos>                        case split  c = 0  /  c != 0
    PRE <term> <eos>                            preimage of a constant
    ONTO <row> <variable> <eos>                 replace f(y) by y (surjectivity)

``MoveGrammar`` says, after any prefix of a move, which tokens may come next,
so that constrained decoding can only ever produce well-formed moves that
refer to things existing in the state. Whether a well-formed move is *legal*
is still decided by the checker.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from . import terms as T
from .algebra import Poly, leading_mono, poly_term
from .checker import State, _single_atom
from .moves import Move, Onto, Pre, Split, SplitNZ, Subst

MAX_ROWS_SHOWN = 14
MAX_STATE_TOKENS = 360
MAX_TERM_TOKENS = 12        # tokens in one term written by the network
MAX_MOVE_TOKENS = 2 + 3 * (1 + MAX_TERM_TOKENS) + 1
MAX_LEAF_INT = 6

SPECIALS = ["<pad>", "<bos>", "<eos>"]
STRUCTURE = ["DOM_R", "DOM_Q", "SOLVE", "GOAL", "P", "NZ", "INJ", "SURJ", "ODD", "EVEN", "ADD", "INVOL", "WIT", "CASES"]
ROW_LABELS = [f"R{i}" for i in range(1, MAX_ROWS_SHOWN + 1)]
OPERATORS = ["+", "-", "*", "~", "^", "/", "f"]
VARIABLES = ["x", "y", "z"]
WITNESSES = ["a", "b", "c"]
INTEGERS = [str(i) for i in range(T.MAX_INT_TOKEN + 1)] + [T.BIG_INT]
HEADS = ["SUB", "SPLIT", "SPLITNZ", "PRE", "ONTO"]

VOCAB = SPECIALS + STRUCTURE + ROW_LABELS + OPERATORS + VARIABLES + WITNESSES + INTEGERS + HEADS
TOKEN_ID = {tok: i for i, tok in enumerate(VOCAB)}
PAD, BOS, EOS = TOKEN_ID["<pad>"], TOKEN_ID["<bos>"], TOKEN_ID["<eos>"]
VOCAB_SIZE = len(VOCAB)

PROP_TOKEN = {"injective": "INJ", "surjective": "SURJ", "odd": "ODD", "even": "EVEN", "additive": "ADD",
              "involution": "INVOL"}


def poly_tokens(poly: Poly) -> list[str]:
    return T.to_prefix(poly_term(poly))


@dataclass
class StateView:
    """What the network is shown of a state, and how its row labels map back to the checker's rows."""

    tokens: list                       # token ids
    row_index: dict                    # label (e.g. "R2") -> index into branch.rows
    row_vars: dict                     # label -> sorted variable names of that row
    splittable: list                   # labels of facts about constants that could be case-split
    p_vars: list                       # variables of the original equation
    witnesses: list
    surjective: bool
    label_of: dict = field(default_factory=dict)   # row index -> label


def _hidden_renaming(row: Poly, rows: set) -> bool:
    """One-variable identities exist once per variable; show only the first copy."""
    names = row.variables()
    if len(names) != 1:
        return False
    (name,) = names
    return any(other < name and row.subst({name: Poly.var(other)}) in rows for other in VARIABLES)


def encode_state(state: State, goal: Optional[Poly] = None) -> StateView:
    """Tokenise the current branch of ``state``.

    ``goal`` is None for the real task ("solve the problem") or an identity
    to derive (used for hindsight training examples).
    """
    branch = state.current
    out = ["<bos>", f"DOM_{branch.domain}"]
    if goal is None:
        out.append("SOLVE")
    else:
        out.append("GOAL")
        out.extend(poly_tokens(goal))
    out.extend(PROP_TOKEN[p] for p in sorted(branch.props))
    out.extend(["WIT"] + list(branch.witnesses) if branch.witnesses else [])
    if len(state.branches) > 1:
        out.extend(["CASES", str(min(len(state.branches) - 1, T.MAX_INT_TOKEN))])
    out.append("P")
    out.extend(poly_tokens(state.problem.poly))
    for known in branch.nonzero:
        out.append("NZ")
        out.extend(poly_tokens(known))

    row_index, row_vars, splittable, label_of = {}, {}, [], {}
    all_rows = set(branch.rows)
    shown = 0
    for index, row in enumerate(branch.rows):
        if shown >= MAX_ROWS_SHOWN:
            break
        if _hidden_renaming(row, all_rows):
            continue
        piece = poly_tokens(row)
        if len(out) + 1 + len(piece) > MAX_STATE_TOKENS:
            break
        label = ROW_LABELS[shown]
        shown += 1
        out.append(label)
        out.extend(piece)
        row_index[label] = index
        label_of[index] = label
        names = sorted(row.variables())
        row_vars[label] = names
        if not names and _single_atom(leading_mono(row)) is None:
            splittable.append(label)
    return StateView(
        tokens=[TOKEN_ID[t] for t in out], row_index=row_index, row_vars=row_vars, splittable=splittable,
        p_vars=sorted(state.problem.poly.variables()), witnesses=list(branch.witnesses),
        surjective="surjective" in branch.props, label_of=label_of,
    )


# ---------------------------------------------------------------------------
# Moves <-> tokens
# ---------------------------------------------------------------------------

def _target_token(target, view: StateView) -> Optional[str]:
    if target == "P":
        return "P"
    if isinstance(target, int):
        return view.label_of.get(target)
    return None


def encode_move(move: Move, view: StateView) -> Optional[list]:
    """Token ids for a creative move, ending in <eos>; None if it cannot be written
    (free moves, quoted targets, hidden rows, numbers too large for the vocabulary)."""
    out: list[str] = []
    if isinstance(move, Subst):
        target = _target_token(move.target, view)
        if target is None:
            return None
        out = ["SUB", target]
        for name, term in sorted(move.bindings, key=lambda b: b[0]):
            out.append(name)
            out.extend(T.to_prefix(term))
    elif isinstance(move, Split):
        target = _target_token(move.target, view)
        if target is None or target == "P" or move.factors:
            return None
        out = ["SPLIT", target]
    elif isinstance(move, SplitNZ):
        out = ["SPLITNZ"] + T.to_prefix(move.term)
    elif isinstance(move, Pre):
        out = ["PRE"] + T.to_prefix(move.term)
    elif isinstance(move, Onto):
        target = _target_token(move.target, view)
        if target is None or target == "P":
            return None
        out = ["ONTO", target, move.var]
    else:
        return None
    out.append("<eos>")
    if T.BIG_INT in out or any(tok not in TOKEN_ID for tok in out):
        return None
    return [TOKEN_ID[t] for t in out]


def decode_move(ids: list, view: StateView) -> Move:
    """Inverse of ``encode_move``. Raises ``ParseError`` on malformed input."""
    toks = [VOCAB[i] for i in ids]
    if toks and toks[-1] == "<eos>":
        toks = toks[:-1]
    if not toks:
        raise T.ParseError("empty move")
    head, rest = toks[0], toks[1:]

    def target_of(tok):
        if tok == "P":
            return "P"
        if tok in view.row_index:
            return view.row_index[tok]
        raise T.ParseError(f"unknown target {tok!r}")

    if head == "SUB":
        if not rest:
            raise T.ParseError("SUB needs a target")
        target = target_of(rest[0])
        bindings = []
        pos = 1
        while pos < len(rest):
            name = rest[pos]
            if name not in VARIABLES:
                raise T.ParseError(f"expected a variable, found {name!r}")
            term, pos = T._from_prefix(rest, pos + 1)
            bindings.append((name, term))
        if not bindings:
            raise T.ParseError("SUB needs at least one binding")
        return Subst(target, tuple(bindings))
    if head == "SPLIT" and len(rest) == 1 and rest[0] != "P":
        return Split(target_of(rest[0]))
    if head == "SPLITNZ":
        return SplitNZ(T.from_prefix(rest))
    if head == "PRE":
        return Pre(T.from_prefix(rest))
    if head == "ONTO" and len(rest) == 2 and rest[0] != "P" and rest[1] in VARIABLES:
        return Onto(target_of(rest[0]), rest[1])
    raise T.ParseError(f"malformed move: {' '.join(toks)}")


# ---------------------------------------------------------------------------
# Grammar for constrained decoding
# ---------------------------------------------------------------------------

_LEAF_INTS = [str(i) for i in range(MAX_LEAF_INT + 1)]
_EXPONENTS = ["2", "3"]
_NUMERATORS = ["1", "2", "3", "4", "5"]
_DENOMINATORS = ["2", "3", "4"]


class MoveGrammar:
    """Tracks a partially written move and lists the tokens allowed next.

    Usage: call ``allowed()`` to get token ids, pick one, call ``advance``;
    stop when ``done``. Any sequence produced this way decodes to a move.
    """

    def __init__(self, view: StateView):
        self.view = view
        self.mode = "head"
        self.done = False
        self.ids: list = []
        self._target: Optional[str] = None
        self._bound: list = []
        self._ground = False
        self._slots: list = []     # pending operand kinds for the term being written
        self._used = 0             # tokens used by the term being written
        self._after_term = ""

    # -- helpers ------------------------------------------------------------

    def _sub_targets(self) -> list:
        out = ["P"] if self.view.p_vars else []
        return out + [label for label, names in self.view.row_vars.items() if names]

    def _begin_term(self, ground: bool, after: str) -> None:
        self.mode = "term"
        self._ground = ground
        self._slots = ["term"]
        self._used = 0
        self._after_term = after

    def _term_tokens(self) -> list:
        kind = self._slots[-1]
        if kind == "exp":
            return _EXPONENTS
        if kind == "num":
            return _NUMERATORS
        if kind == "den":
            return _DENOMINATORS
        room = MAX_TERM_TOKENS - self._used - 1 - (len(self._slots) - 1)  # tokens left after this one, beyond what is owed
        out = list(_LEAF_INTS) + list(self.view.witnesses)
        if not self._ground:
            out += self.view.p_vars if self._target == "P" else sorted(set(self.view.p_vars) | {"x", "y"})
        if room >= 1:
            out += ["f", "~"]
        if room >= 2:
            out += ["+", "-", "*", "^", "/"]
        return out

    # -- interface ----------------------------------------------------------

    def allowed_tokens(self) -> list:
        if self.done:
            return []
        mode = self.mode
        if mode == "head":
            out = []
            if self._sub_targets():
                out.append("SUB")
            if self.view.splittable:
                out.append("SPLIT")
            out.append("SPLITNZ")
            if self.view.surjective:
                out.append("PRE")
                if any(self.view.row_vars.values()):
                    out.append("ONTO")
            return out
        if mode == "sub_target":
            return self._sub_targets()
        if mode == "split_target":
            return list(self.view.splittable)
        if mode == "onto_target":
            return [label for label, names in self.view.row_vars.items() if names]
        if mode == "onto_var":
            return list(self.view.row_vars[self._target])
        if mode == "binding":
            names = self.view.p_vars if self._target == "P" else self.view.row_vars[self._target]
            remaining = [n for n in names if not self._bound or n > self._bound[-1]]
            return remaining + (["<eos>"] if self._bound else [])
        if mode == "term":
            return self._term_tokens()
        if mode == "eos":
            return ["<eos>"]
        raise AssertionError(mode)

    def allowed(self) -> list:
        return [TOKEN_ID[t] for t in self.allowed_tokens()]

    def advance(self, token_id: int) -> None:
        tok = VOCAB[token_id]
        if tok not in self.allowed_tokens():
            raise ValueError(f"token {tok!r} is not allowed here")
        self.ids.append(token_id)
        mode = self.mode
        if mode == "head":
            if tok == "SUB":
                self.mode = "sub_target"
            elif tok == "SPLIT":
                self.mode = "split_target"
            elif tok == "ONTO":
                self.mode = "onto_target"
            else:  # SPLITNZ, PRE
                self._begin_term(ground=True, after="eos")
        elif mode == "sub_target":
            self._target = tok
            self.mode = "binding"
        elif mode == "split_target":
            self.mode = "eos"
        elif mode == "onto_target":
            self._target = tok
            self.mode = "onto_var"
        elif mode == "onto_var":
            self.mode = "eos"
        elif mode == "binding":
            if tok == "<eos>":
                self.done = True
            else:
                self._bound.append(tok)
                self._begin_term(ground=False, after="binding")
        elif mode == "term":
            self._used += 1
            self._slots.pop()
            if tok in ("f", "~"):
                self._slots.append("term")
            elif tok in ("+", "-", "*"):
                self._slots += ["term", "term"]
            elif tok == "^":
                self._slots += ["exp", "term"]      # popped last-in-first-out: term, then exponent
            elif tok == "/":
                self._slots += ["den", "num"]
            if not self._slots:
                self.mode = self._after_term
        elif mode == "eos":
            self.done = True


def sample_uniform(view: StateView, rng) -> tuple[list, float]:
    """A random well-formed move: each token uniform among those the grammar allows.

    Returns (token ids, log-probability under this uniform policy).
    """
    import math

    grammar = MoveGrammar(view)
    logp = 0.0
    while not grammar.done:
        options = grammar.allowed()
        logp -= math.log(len(options))
        grammar.advance(rng.choice(options))
    return grammar.ids, logp
