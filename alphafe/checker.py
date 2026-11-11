"""The proof checker: the only trusted part of AlphaFE.

The network (or a person, or brute force) *proposes* moves; this module
*decides* whether each one is a valid deduction. "Solved" means every move of
a proof was accepted here and no case is left open. All arithmetic is exact.

Proof state
-----------
A ``State`` is a stack of open case *branches* plus the solutions collected
from branches that are already closed. Moves act on the first open branch.
A ``Branch`` knows:

* ``rows``     identities that hold for all values of their variables,
               stored in a reduced form (see below); identities without
               variables are facts about constants such as f(0)^2 = f(0);
* ``nonzero``  constants proven (or assumed, in this case) to be nonzero;
* ``props``    proven properties: injective, surjective, odd, even,
               additive, involution;
* ``witnesses`` named constants introduced by surjectivity.

Automatic normalisation
-----------------------
Each new identity is simplified with steps that are valid deductions in their
own right, so that proofs do not have to spell them out:

* *linear elimination*: the rows are kept in reduced echelon form over the
  rationals, i.e. each row is solved for its leading monomial and that
  monomial is eliminated from every other row (adding rational multiples of
  true identities gives true identities);
* *rewriting (congruence)*: a row ``A = rest`` whose leading monomial is a
  single atom A lets us replace A by ``rest`` anywhere, including inside
  f(...), because equal arguments give equal values;
* *property rewriting*: odd, even, additive and involution are applied to
  every matching f(...);
* *coefficient extraction*: if an identity contains no f of a variable, it is
  a polynomial in the variables vanishing on an infinite field, so each of its
  coefficients vanishes;
* *cancelling a variable*: from ``x * Q = 0`` for all x we get Q = 0 for
  x != 0, and if Q is also known to vanish at x = 0 then Q = 0 for all x;
* *dividing by a proven-nonzero constant*;
* *renaming*: an identity in a single variable is also recorded with that
  variable renamed to each other variable in use;
* *contradictions*: ``1 = 0``, a constant assumed nonzero that became zero, or
  a polynomial equation in one constant with no root in the domain.

Soundness traps (see tests/test_traps.py)
-----------------------------------------
* case splits only on facts without variables (no pointwise trap);
* f is cancelled only when injectivity has been established;
* preimages are taken only when surjectivity has been established;
* division only by constants proven nonzero;
* "additive implies linear" only over Q;
* case splits are checked to be exhaustive by re-multiplying the factors;
* every reported solution is substituted back into the original equation.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Optional

from . import terms as T
from .algebra import (
    ONE,
    Poly,
    Unsupported,
    ZERO,
    atom_vars,
    div_exact,
    equation_poly,
    equation_str,
    factor_hint,
    has_no_root,
    has_var_f,
    leading_mono,
    mono_rank,
    monic,
    poly_size,
    poly_str,
    split_by_vars,
    to_poly,
    unique_root,
    univariate_coeffs,
)
from .moves import (
    Cancel,
    Cauchy,
    Conclude,
    Divide,
    EqRef,
    Inj,
    Move,
    Onto,
    Pre,
    Quadratic,
    Split,
    SplitNZ,
    Subst,
    Surj,
    show_move,
)
from .solutions import SolutionSet, fit_candidate, make_solution_set, verify

NORM_PASSES = 30        # cap on rewriting passes (termination guard, not soundness)
WORK_BUDGET = 400       # cap on normalisation work per move
MAX_ROWS = 40           # identities per branch
MAX_POLY_TERMS = 80     # monomials per identity
MAX_POLY_SIZE = 400     # structural size per identity
MAX_TERM_SIZE = 40      # nodes in a substituted term
MAX_WITNESSES = 3
MAX_BRANCHES = 16
WITNESS_NAMES = "abcde"
PROPERTIES = ("injective", "surjective", "odd", "even", "additive", "involution")
X = Poly.var("x")


class Reject(Exception):
    """A move was refused; ``reason`` says why."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


class _Closed(Exception):
    """Internal: the current branch has been refuted."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


# ---------------------------------------------------------------------------
# Problems
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Problem:
    """Find all f: D -> D with ``equation`` for all values of its variables."""

    equation: str
    domain: str
    poly: Poly = field(compare=False, repr=False)
    name: str = ""

    @staticmethod
    def parse(equation: str, domain: str = "R", name: str = "") -> "Problem":
        if domain not in ("R", "Q"):
            raise ValueError("domain must be 'R' or 'Q'")
        lhs, rhs = T.parse_equation(equation)
        symbols = sorted(T.term_syms(lhs) | T.term_syms(rhs))
        if symbols:
            raise ValueError(f"the equation may only use the variables {', '.join(T.VAR_NAMES)}, numbers and f; "
                             f"it also uses {', '.join(symbols)} (f is the only function: g(x) is read as g times x)")
        poly = to_poly(lhs) - to_poly(rhs)
        if poly.is_zero():
            raise ValueError("the equation holds for every function: both sides are equal")
        if not poly.variables():
            raise ValueError("the equation needs at least one variable")
        if len(poly.variables()) > 3:
            raise ValueError(f"the equation has {len(poly.variables())} variables; at most 3 are supported")
        if not any(a[0] == "f" for a in poly.top_atoms()):
            raise ValueError("the equation does not involve f")
        return Problem(equation.strip(), domain, poly, name)

    def standard_names(self) -> tuple["Problem", dict]:
        """The same problem written with the variables x, y, z, and the renaming used ({old: new}).

        The checker accepts the letters x y z t u v w. The network's
        vocabulary has only x, y and z, so problems are renamed before a
        network search. Letters that are already x, y or z keep their name;
        the others take the unused ones in order. Returns ``(self, {})`` when
        there is nothing to rename.
        """
        mine = sorted(self.poly.variables())
        free = [name for name in "xyz" if name not in mine]
        names = {old: free.pop(0) for old in mine if old not in "xyz"}
        if not names:
            return self, {}
        lhs, rhs = T.parse_equation(self.equation)
        text = T.show_equation(T.rename_vars(lhs, names), T.rename_vars(rhs, names))
        return Problem.parse(text, self.domain, self.name), names

    def __str__(self) -> str:
        return f"f: {self.domain} -> {self.domain}, {self.equation}"


# ---------------------------------------------------------------------------
# One case branch
# ---------------------------------------------------------------------------

def _single_atom(mono) -> Optional[tuple]:
    """The atom if ``mono`` is a single atom to the first power, else None."""
    if len(mono) == 1 and mono[0][1] == 1:
        return mono[0][0]
    return None


def _leading_negative(poly: Poly) -> bool:
    return poly.key[0][1] < 0


def detect_property(row: Poly) -> Optional[str]:
    """Recognise the defining identity of a named property.

    odd: f(-x) = -f(x);  even: f(-x) = f(x);  involution: f(f(x)) = x;
    additive: f(x + y) = f(x) + f(y).
    """
    names = sorted(row.variables())
    if len(names) == 1:
        v = Poly.var(names[0])
        if row == monic(Poly.f(-v) + Poly.f(v)):
            return "odd"
        if row == monic(Poly.f(-v) - Poly.f(v)):
            return "even"
        if row == monic(Poly.f(Poly.f(v)) - v):
            return "involution"
    elif len(names) == 2:
        u, v = Poly.var(names[0]), Poly.var(names[1])
        if row == monic(Poly.f(u + v) - Poly.f(u) - Poly.f(v)):
            return "additive"
    return None


class Branch:
    """The facts known in one case of the proof. See the module docstring."""

    __slots__ = ("domain", "names", "rows", "nonzero", "props", "witnesses", "case", "assumptions", "_pivots", "_rules")

    def __init__(self, domain: str, names: tuple = ("x", "y")):
        self.domain = domain
        self.names = names             # the variable names in use
        self.rows: list[Poly] = []
        self.nonzero: list[Poly] = []
        self.props: set[str] = set()
        self.witnesses: list[str] = []
        self.case: tuple = ()          # human-readable case path
        self.assumptions: list = []    # ("zero", p) / ("nonzero", p) / ("witness", name, p)
        self._pivots: dict = {}
        self._rules: dict = {}

    def copy(self) -> "Branch":
        new = Branch(self.domain, self.names)
        new.rows = list(self.rows)
        new.nonzero = list(self.nonzero)
        new.props = set(self.props)
        new.witnesses = list(self.witnesses)
        new.case = self.case
        new.assumptions = list(self.assumptions)
        new._pivots = dict(self._pivots)
        new._rules = dict(self._rules)
        return new

    def signature(self) -> tuple:
        """Hashable summary of everything known; equal signatures mean equal knowledge."""
        return (frozenset(self.rows), frozenset(self.props), frozenset(self.nonzero), len(self.witnesses))

    # -- normalisation ------------------------------------------------------

    def _reindex(self) -> None:
        self._pivots = {}
        self._rules = {}
        for row in self.rows:
            lead = leading_mono(row)
            self._pivots[lead] = row
            atom = _single_atom(lead)
            if atom is not None:
                # row is  atom + rest = 0,  so  atom = -rest
                self._rules[atom] = Poly({lead: ONE}) - row

    def _rewrite_atom(self, atom) -> Optional[Poly]:
        rule = self._rules.get(atom)
        if rule is not None:
            return rule
        props = self.props
        if atom[0] != "f" or not props:
            return None
        arg = Poly.from_key(atom[1])
        if "involution" in props and len(arg.terms) == 1:
            # f(f(B)) = B
            (mono, coef), = arg.terms.items()
            inner = _single_atom(mono)
            if coef == 1 and inner is not None and inner[0] == "f":
                return Poly.from_key(inner[1])
        if "additive" in props:
            # f(q1*m1 + q2*m2 + ...) = q1*f(m1) + q2*f(m2) + ...  (additive
            # functions are linear over the rationals, on R as well as on Q)
            if not arg.terms:
                return ZERO
            if len(arg.terms) > 1 or next(iter(arg.terms.values())) != 1:
                out = ZERO
                for mono, coef in arg.terms.items():
                    out = out + Poly.f(Poly({mono: ONE})).scale(coef)
                return out
            return None
        if "odd" in props:
            if not arg.terms:
                return ZERO  # f(0) = -f(0)
            if _leading_negative(arg):
                return -Poly.f(-arg)
        if "even" in props and arg.terms and _leading_negative(arg):
            return Poly.f(-arg)
        return None

    def norm(self, poly: Poly) -> Poly:
        """Rewrite with the rules and properties until nothing changes."""
        if not self._rules and not self.props:
            return poly
        for _ in range(NORM_PASSES):
            new = poly.rewrite(self._rewrite_atom)
            if new is poly or new == poly:
                return poly
            poly = new
        raise Reject("normalisation did not converge")

    def reduce(self, poly: Poly) -> Poly:
        """Eliminate the leading monomials of the rows from ``poly``."""
        pivots = self._pivots
        hits = [mono for mono in poly.terms if mono in pivots]
        for mono in hits:
            coef = poly.terms.get(mono)
            if coef:
                poly = poly - pivots[mono].scale(coef)
        return poly

    def normal_form(self, poly: Poly) -> Poly:
        for _ in range(NORM_PASSES):
            new = self.reduce(self.norm(poly))
            if new is poly or new == poly:
                return new
            poly = new
        raise Reject("normalisation did not converge")

    def known_zero(self, poly: Poly) -> bool:
        """Does ``poly = 0`` follow from the rows by rewriting and elimination?"""
        return self.normal_form(poly).is_zero()

    def known_nonzero(self, poly: Poly) -> bool:
        """Is the constant ``poly`` proven nonzero in this branch?"""
        if poly.variables():
            return False
        poly = self.normal_form(poly)
        value = poly.const_value()
        if value is not None:
            return value != 0
        for known in self.nonzero:
            ratio = div_exact(poly, known)
            if ratio is not None and ratio.const_value() not in (None, 0):
                return True
        return False

    # -- adding facts -------------------------------------------------------

    def add(self, polys) -> None:
        """Add identities ``p = 0`` and re-establish the normal form.

        Raises ``_Closed`` if a contradiction appears, ``Reject`` if the
        result is too large or normalisation does not settle.
        """
        queue = deque(polys)
        budget = WORK_BUDGET
        while True:
            while queue:
                budget -= 1
                if budget < 0:
                    raise Reject("normalisation did not converge")
                poly = self.normal_form(queue.popleft())
                if poly.is_zero():
                    continue
                value = poly.const_value()
                if value is not None:
                    raise _Closed(f"{value} = 0")
                # One unknown quantity (a constant, or a value such as f(x))
                # satisfying a polynomial equation with no root in the domain.
                uni = univariate_coeffs(poly)
                if uni is not None:
                    if has_no_root(uni[1], self.domain):
                        raise _Closed(f"{equation_str(poly)} has no solution in {self.domain}")
                    # ... or with exactly one root there: no choice, so it IS that root.
                    # (Two roots would be the pointwise trap; nothing is deduced then.)
                    if len(uni[1]) > 2:
                        root = unique_root(uni[1], self.domain)
                        if root is not None:
                            queue.append(Poly.atom(uni[0]) - root)
                            continue
                names = poly.variables()
                if names:
                    if not has_var_f(poly):
                        # A polynomial in the variables that vanishes identically.
                        queue.extend(split_by_vars(poly).values())
                        continue
                    quotient = self._cancel_variable(poly, names)
                    if quotient is not None:
                        queue.append(quotient)
                        continue
                quotient = self._divide_nonzero(poly)
                if quotient is not None:
                    queue.append(quotient)
                    continue
                self._insert(poly, queue)
            # New facts about constants can make an old identity x*Q = 0
            # cancellable (Q(0) = 0 may only now be known): look again.
            for row in self.rows:
                names = row.variables()
                quotient = self._cancel_variable(row, names) if names else None
                if quotient is not None:
                    self.rows = [r for r in self.rows if r is not row]
                    self._reindex()
                    queue.append(quotient)
                    break
            else:
                break
        self.rows.sort(key=lambda row: mono_rank(leading_mono(row)))

    def _cancel_variable(self, poly: Poly, names) -> Optional[Poly]:
        """If poly = v * Q and Q is known to vanish at v = 0, return Q."""
        for name in sorted(names):
            atom = ("v", name)
            if all(any(a == atom for a, _ in mono) for mono in poly.terms):
                quotient = div_exact(poly, Poly.atom(atom))
                if quotient is not None and self.known_zero(quotient.subst({name: ZERO})):
                    return quotient
        return None

    def _divide_nonzero(self, poly: Poly) -> Optional[Poly]:
        for known in self.nonzero:
            quotient = div_exact(poly, known)
            if quotient is not None:
                return quotient
        return None

    def _insert(self, poly: Poly, queue: deque) -> None:
        if len(poly.terms) > MAX_POLY_TERMS or poly_size(poly) > MAX_POLY_SIZE:
            raise Reject("identity too large")
        poly = monic(poly)
        lead = leading_mono(poly)
        # Eliminate the new leading monomial from the existing rows. Rows that
        # change go back through the queue so they are fully re-examined.
        kept = []
        for row in self.rows:
            coef = row.terms.get(lead)
            if coef:
                queue.append(row - poly.scale(coef))
            else:
                kept.append(row)
        kept.append(poly)
        self.rows = kept
        if len(self.rows) > MAX_ROWS:
            raise Reject("too many identities")
        self._reindex()

        # An identity in one variable holds for every value of it, so it holds
        # with the variable renamed: f(2x) = 2f(x) also gives f(2y) = 2f(y).
        own = poly.variables()
        if len(own) == 1:
            (name,) = own
            for other in self.names:
                if other != name:
                    queue.append(poly.subst({name: Poly.var(other)}))

        prop = detect_property(poly)
        if prop is not None and prop not in self.props:
            self.props.add(prop)
            if prop == "involution":
                # f(f(x)) = x: f(a) = f(b) gives a = f(f(a)) = f(f(b)) = b, and
                # every y equals f(f(y)).
                self.props.update(("injective", "surjective"))
            self._requeue_all(queue)
            return
        atom = _single_atom(lead)
        if atom is not None:
            # A new rewrite rule: rows mentioning the atom elsewhere (inside
            # f(...) or in a product) must be rewritten.
            kept, redo = [], []
            for row in self.rows:
                (redo if row is not poly and row.contains_atom(atom) else kept).append(row)
            if redo:
                self.rows = kept
                self._reindex()
                queue.extend(redo)
            self._renormalise_nonzero()

    def _requeue_all(self, queue: deque) -> None:
        rows, self.rows = self.rows, []
        self._reindex()
        queue.extend(rows)
        self._renormalise_nonzero()

    def _renormalise_nonzero(self) -> None:
        updated = []
        for known in self.nonzero:
            known = self.normal_form(known)
            if known.is_zero():
                raise _Closed("a constant assumed nonzero is zero")
            if known.const_value() is None and known not in updated:
                updated.append(known)
        self.nonzero = updated

    def assume_nonzero(self, poly: Poly) -> None:
        self.nonzero.append(poly)
        queue: deque = deque()
        self._requeue_all(queue)
        self.add(queue)


# ---------------------------------------------------------------------------
# States and the log
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LogEntry:
    """What one move did; consumed by the renderer."""

    move: Optional[Move]
    case: tuple = ()
    instance: Optional[Poly] = None      # the substituted identity, lightly simplified
    source: Optional[Poly] = None        # the identity a move acted on
    new_rows: tuple = ()                 # every identity that is new or changed
    fresh_rows: tuple = ()               # ... those solved for a monomial not solved for before
    new_props: tuple = ()
    closed: Optional[str] = None         # "contradiction" | "concluded"
    reason: str = ""
    candidate: Optional[Poly] = None     # f(x) = candidate, before pinning constants
    solutions: tuple = ()
    children: tuple = ()                 # for splits: (label, closed_reason or None)
    witness: Optional[str] = None
    extra: Optional[Poly] = None


class State:
    """An immutable proof state: open branches, collected solutions, and a log."""

    __slots__ = ("problem", "branches", "solutions", "log")

    def __init__(self, problem: Problem, branches: tuple, solutions: tuple, log: tuple):
        self.problem = problem
        self.branches = branches
        self.solutions = solutions
        self.log = log

    @property
    def solved(self) -> bool:
        return not self.branches

    @property
    def current(self) -> Branch:
        return self.branches[0]

    @property
    def solution_set(self) -> SolutionSet:
        return make_solution_set(self.solutions)

    def key(self) -> tuple:
        return (tuple(b.signature() for b in self.branches), frozenset(self.solutions))


LOAD_REFUSED = "the checker cannot load the equation"


def initial_state(problem: Problem) -> State:
    """The state holding only the problem's equation.

    Raises ``Reject`` when the equation itself is over the size caps that
    apply to every identity (``MAX_POLY_TERMS``, ``MAX_POLY_SIZE``). The caps
    are not lifted for the original equation: substitutions into it would
    produce identities of the same size. Callers that score problems treat
    this as "not solved" (``check``, ``env.try_start``).
    """
    branch = Branch(problem.domain, tuple(sorted(problem.poly.variables() | {"x", "y"})))
    try:
        branch.add([problem.poly])
    except _Closed as closed:
        entry = LogEntry(None, closed="contradiction", reason=closed.reason)
        return State(problem, (), (), (entry,))
    entry = LogEntry(None, new_rows=tuple(branch.rows), new_props=tuple(sorted(branch.props)))
    return State(problem, (branch,), (), (entry,))


# ---------------------------------------------------------------------------
# Helpers shared by the moves
# ---------------------------------------------------------------------------

def _term_poly(state: State, branch: Branch, term: T.Term, ground: bool = False) -> Poly:
    """Canonicalise a term written in a move, checking its symbols are legal."""
    if T.term_size(term) > MAX_TERM_SIZE:
        raise Reject("term too large")
    unknown = T.term_syms(term) - set(branch.witnesses)
    if unknown:
        raise Reject(f"unknown constant {sorted(unknown)[0]!r} (only witnesses introduced by 'pre' may be used)")
    allowed = set("xyz") | set(state.problem.poly.variables())
    bad = T.term_vars(term) - allowed
    if bad:
        raise Reject(f"variable {sorted(bad)[0]!r} is not available")
    if ground and T.term_vars(term):
        raise Reject("this term must not contain variables")
    for sub in T.subterms(term):
        if isinstance(sub, T.Pow) and sub.exp > 6:
            raise Reject("exponent too large")
    return to_poly(term)


def _resolve(state: State, branch: Branch, target) -> Poly:
    """The identity a target refers to (always something known to be true here)."""
    if target == "P":
        return state.problem.poly
    if isinstance(target, int) and not isinstance(target, bool):
        if not 0 <= target < len(branch.rows):
            raise Reject(f"there is no identity R{target + 1}")
        return branch.rows[target]
    if isinstance(target, EqRef):
        for side in (target.lhs, target.rhs):
            _term_poly(state, branch, side)
        poly = to_poly(target.lhs) - to_poly(target.rhs)
        if poly.is_zero():
            raise Reject("the quoted identity is trivial")
        if not branch.known_zero(poly):
            raise Reject("the quoted identity is not known")
        return poly
    raise Reject("bad target")


def _candidates(state: State, branch: Branch, target) -> list[Poly]:
    """Identities to try for a move whose target is optional: the given one,
    or else every current identity followed by the original equation."""
    if target is not None:
        return [_resolve(state, branch, target)]
    out = list(branch.rows)
    if state.problem.poly not in out:
        out.append(state.problem.poly)
    return out


def injectivity_variable(branch: Branch, poly: Poly) -> Optional[str]:
    """Find a variable v witnessing injectivity in ``poly = 0``.

    Criterion: after replacing every occurrence of f(v) by a fresh symbol t,
    the identity reads  alpha*v + R(t, other variables) = 0  with alpha a
    proven-nonzero constant and R free of v. Then f(a) = f(b) makes R take the
    same value at v = a and v = b, so alpha*a = alpha*b and a = b.
    """
    fresh = Poly.named("#t")
    for name in sorted(poly.variables()):
        v = ("v", name)
        replaced = poly.replace_atoms({("f", Poly.var(name).key): fresh})
        coeffs = replaced.coeffs_in(v)
        if set(coeffs) - {0, 1} or 1 not in coeffs:
            continue
        alpha, rest = coeffs[1], coeffs.get(0, ZERO)
        if name in rest.variables():
            continue
        if alpha.variables() or alpha.contains_atom(("c", "#t")):
            continue
        if branch.known_nonzero(alpha):
            return name
    return None


def surjectivity_variable(branch: Branch, poly: Poly) -> Optional[str]:
    """Find a variable v witnessing surjectivity in ``poly = 0``.

    Criterion: the identity reads  beta*f(T) + alpha*v + H = 0  with beta a
    nonzero rational, alpha a proven-nonzero constant and H free of v. Fix the
    other variables; as v runs over the domain, -(alpha*v + H)/beta runs over
    the whole domain, and each of those values is f of something.
    """
    for name in sorted(poly.variables()):
        coeffs = poly.coeffs_in(("v", name))
        if set(coeffs) - {0, 1} or 1 not in coeffs:
            continue
        alpha, rest = coeffs[1], coeffs.get(0, ZERO)
        if alpha.variables() or not branch.known_nonzero(alpha):
            continue
        for mono, coef in rest.terms.items():
            atom = _single_atom(mono)
            if atom is not None and atom[0] == "f":
                others = rest - Poly({mono: coef})
                if name not in others.variables():
                    return name
    return None


def _f_values(poly: Poly):
    """Yield (A, V) for every way of reading ``poly = 0`` as f(A) = V, where
    f(A) is a lone monomial and V is everything else."""
    for mono, coef in poly.terms.items():
        atom = _single_atom(mono)
        if atom is not None and atom[0] == "f":
            yield atom, (Poly({mono: coef}) - poly).scale(1 / coef)


def cancel_results(branch: Branch, poly: Poly):
    """Everything injectivity gives from ``poly = 0`` (a generator of new identities).

    * beta*(f(A) - f(B)) = 0 gives A = B;
    * f(A) = V, where V is a constant known to equal f(g), gives A = g;
    * f(A) = V together with another current identity f(B) = V (the same V)
      gives A = B.
    """
    if len(poly.terms) == 2:
        (m1, c1), (m2, c2) = poly.terms.items()
        a1, a2 = _single_atom(m1), _single_atom(m2)
        if a1 is not None and a2 is not None and a1[0] == "f" and a2[0] == "f" and c1 + c2 == 0:
            yield Poly.from_key(a1[1]) - Poly.from_key(a2[1])
    for atom, value in _f_values(poly):
        if not atom_vars(atom):
            continue
        if not value.variables():
            for known, image in branch._rules.items():
                if known[0] == "f" and not atom_vars(known) and image == value:
                    yield Poly.from_key(atom[1]) - Poly.from_key(known[1])
        for row in branch.rows:
            for other, other_value in _f_values(row):
                if other != atom and other_value == value:
                    yield Poly.from_key(atom[1]) - Poly.from_key(other[1])


def cauchy_form(poly: Poly) -> Optional[tuple]:
    """Read ``poly = 0`` as  f(u + v) = f(u) + f(v) + q(u, v)  with q a polynomial.

    Returns (p, q0) such that g = f - p satisfies g(u + v) = g(u) + g(v) + q0,
    where p is a polynomial in x without constant or linear term and q0 is a
    constant; or None if the identity does not have this shape.

    How p is found: (u + v)^k - u^k - v^k contains the monomial k*u^(k-1)*v,
    so the coefficient of u^(k-1)*v in q must be k times the coefficient of
    x^k in p. Having built p from those coefficients, we check that
    q - (p(u + v) - p(u) - p(v)) really is a constant. If it is not, q is not
    of the required kind and we return None.
    """
    names = sorted(poly.variables())
    if len(names) != 2:
        return None
    u, v = Poly.var(names[0]), Poly.var(names[1])
    lead = Poly.f(u + v)
    (mono,) = lead.terms
    coef = poly.terms.get(mono)
    if not coef:
        return None
    defect = (lead - Poly.f(u) - Poly.f(v)) - poly.scale(1 / coef)   # f(u+v) - f(u) - f(v) = defect
    if has_var_f(defect):
        return None
    p = ZERO
    for var_mono, coefficient in split_by_vars(defect).items():
        exps = {atom[1]: e for atom, e in var_mono}
        if exps.get(names[1], 0) == 1 and exps.get(names[0], 0) >= 1:
            k = exps[names[0]] + 1
            p = p + coefficient * (X ** k).scale(Fraction(1, k))
    rebuilt = p.subst({"x": u + v}) - p.subst({"x": u}) - p.subst({"x": v})
    constant = defect - rebuilt
    if constant.variables():
        return None
    return p, constant


def cauchy_constant(poly: Poly) -> Optional[Poly]:
    """If ``poly = 0`` reads f(u + v) = f(u) + f(v) - C with C constant, return C."""
    form = cauchy_form(poly)
    if form is None or not form[0].is_zero():
        return None
    return -form[1]


def is_quadratic_equation(poly: Poly) -> bool:
    """Is ``poly = 0`` the quadratic functional equation f(u+v) + f(u-v) = 2f(u) + 2f(v)?"""
    names = sorted(poly.variables())
    if len(names) != 2:
        return False
    target = monic(poly)
    for first, second in (names, names[::-1]):
        u, v = Poly.var(first), Poly.var(second)
        if target == monic(Poly.f(u + v) + Poly.f(u - v) - Poly.f(u).scale(2) - Poly.f(v).scale(2)):
            return True
    return False


def explicit_form(poly: Poly) -> Optional[Poly]:
    """If ``poly = 0`` determines f explicitly, return E with f(x) = E.

    Required shape: one variable v; exactly one f-atom containing v, namely
    f(a*v + b) with a a nonzero rational and b constant, occurring only as a
    lone monomial with a rational coefficient. Then f(a*v + b) = E0(v) for all
    v, and since a*v + b takes every value, f(x) = E0((x - b)/a) for all x.

    Shapes like x*f(x) = x^2 are *not* accepted: they say nothing at x = 0.
    """
    names = poly.variables()
    if len(names) != 1:
        return None
    (name,) = names
    f_atoms = [a for a in poly.top_atoms() if a[0] == "f" and atom_vars(a)]
    if len(f_atoms) != 1:
        return None
    atom = f_atoms[0]
    mono = ((atom, 1),)
    coef = poly.terms.get(mono)
    if coef is None:
        return None
    rest = poly - Poly({mono: coef})
    if atom in rest.top_atoms():
        return None  # f(...) also appears in a product or a power
    arg = Poly.from_key(atom[1])
    arg_coeffs = arg.coeffs_in(("v", name))
    if set(arg_coeffs) - {0, 1} or 1 not in arg_coeffs:
        return None
    slope = arg_coeffs[1].const_value()
    shift = arg_coeffs.get(0, ZERO)
    if slope is None or slope == 0 or shift.variables():
        return None
    value = rest.scale(-1 / coef)  # f(arg) = value
    return value.subst({name: (X - shift).scale(1 / slope)})


def _parametrise(expr: Poly) -> Poly:
    """Replace each unknown constant (f(0), f(1), a witness, ...) by a parameter."""
    atoms = sorted(a for a in expr.top_atoms() if a != ("v", "x"))
    mapping = {atom: Poly.named(f"k{i}") for i, atom in enumerate(atoms)}
    out = ZERO
    for mono, coef in expr.terms.items():
        product = Poly.const(coef)
        for atom, exp in mono:
            product = product * mapping.get(atom, X) ** exp
        out = out + product
    return out


# ---------------------------------------------------------------------------
# The moves
# ---------------------------------------------------------------------------

class _Outcome:
    """What a move handler hands back to ``apply``."""

    def __init__(self, branches=None, **log):
        self.branches = branches  # None: keep the (mutated) current branch
        self.log = log


def _do_subst(state: State, branch: Branch, move: Subst) -> _Outcome:
    """Substitute terms for variables in a known identity.

    An identity holds for *all* values of its variables, so it still holds
    when the variables are replaced by any expressions, simultaneously.
    """
    target = _resolve(state, branch, move.target)
    mapping = {}
    for name, term in move.bindings:
        if name in mapping:
            raise Reject(f"{name} is bound twice")
        if name not in target.variables():
            raise Reject(f"{name} does not occur in the identity")
        mapping[name] = _term_poly(state, branch, term)
    if not mapping:
        raise Reject("a substitution needs at least one binding")
    instance = target.subst(mapping)
    shown = branch.norm(instance)
    branch.add([instance])
    return _Outcome(instance=shown, source=target)


def _do_split(state: State, branch: Branch, move: Split) -> _Outcome:
    """Case split on a fact about constants that factors.

    If c1 * c2 * ... = 0 where every factor is a constant expression (no
    variables), then one of the factors is zero, and the cases c1 = 0,
    c2 = 0, ... together cover everything. The factorisation is checked by
    multiplying it back out.

    The fact must not contain variables. From "f(x)(f(x) - x) = 0 for every
    x" one may NOT conclude "f = 0 everywhere or f = x everywhere": which
    factor vanishes can depend on x (the pointwise trap).
    """
    poly = _resolve(state, branch, move.target)
    if not isinstance(move.target, int):
        poly = branch.norm(poly)
    if poly.variables():
        raise Reject("case split only on facts about constants: this identity has variables (pointwise trap)")
    if poly.is_zero():
        raise Reject("nothing to split on")
    if move.factors:
        factors = []
        rest = poly
        for term in move.factors:
            factor = branch.norm(_term_poly(state, branch, term, ground=True))
            if factor.const_value() is not None:
                raise Reject("a case factor must not be a plain number")
            quotient = div_exact(rest, factor)
            if quotient is None:
                raise Reject(f"{poly_str(factor)} is not a factor: the split would not be exhaustive")
            while quotient is not None:
                rest = quotient
                quotient = div_exact(rest, factor)
            factors.append(factor)
        if rest.const_value() is None:
            raise Reject("the factors do not multiply to the fact: the split is not exhaustive")
    else:
        hinted = factor_hint(poly)
        product = Poly.const(1)
        for factor, mult in hinted:
            product = product * factor ** mult
        ratio = div_exact(poly, product)
        if ratio is None or ratio.const_value() in (None, 0):
            raise Reject("could not factor this fact")
        if len(hinted) == 1 and hinted[0][1] == 1:
            raise Reject("this fact does not factor")
        factors = [factor for factor, _ in hinted]
    if len(state.branches) - 1 + len(factors) > MAX_BRANCHES:
        raise Reject("too many open cases")
    children, summary = [], []
    for factor in factors:
        child = branch.copy()
        label = equation_str(factor)
        child.case = branch.case + (label,)
        child.assumptions.append(("zero", factor))
        try:
            child.add([factor])
        except _Closed as closed:
            summary.append((label, closed.reason))
            continue
        summary.append((label, None))
        children.append(child)
    return _Outcome(branches=children, source=poly, children=tuple(summary))


def _do_splitnz(state: State, branch: Branch, move: SplitNZ) -> _Outcome:
    """Case split: a constant is zero, or it is not.

    Exhaustive by the law of the excluded middle. In the second case the
    constant joins the proven-nonzero set, which is the licence to divide by it.
    """
    poly = branch.norm(_term_poly(state, branch, move.term, ground=True))
    if poly.const_value() is not None:
        raise Reject("this constant is a known number")
    if branch.known_zero(poly):
        raise Reject("this constant is already known to be zero")
    if branch.known_nonzero(poly):
        raise Reject("this constant is already known to be nonzero")
    if len(state.branches) + 1 > MAX_BRANCHES:
        raise Reject("too many open cases")
    children, summary = [], []
    text = poly_str(poly)

    zero = branch.copy()
    zero.case = branch.case + (equation_str(poly),)
    zero.assumptions.append(("zero", poly))
    try:
        zero.add([poly])
        children.append(zero)
        summary.append((zero.case[-1], None))
    except _Closed as closed:
        summary.append((zero.case[-1], closed.reason))

    nonzero = branch.copy()
    nonzero.case = branch.case + (f"{text} != 0",)
    nonzero.assumptions.append(("nonzero", poly))
    try:
        nonzero.assume_nonzero(poly)
        children.append(nonzero)
        summary.append((nonzero.case[-1], None))
    except _Closed as closed:
        summary.append((nonzero.case[-1], closed.reason))
    return _Outcome(branches=children, source=poly, children=tuple(summary))


def _do_divide(state: State, branch: Branch, move: Divide) -> _Outcome:
    """Divide an identity by a constant that has been proven nonzero.

    If c * Q = 0 and c != 0 then Q = 0. Without a proof that c != 0 this is
    not allowed; use ``splitnz`` to treat c = 0 separately.
    """
    poly = _resolve(state, branch, move.target)
    divisor = branch.norm(_term_poly(state, branch, move.term, ground=True))
    if not branch.known_nonzero(divisor):
        raise Reject(f"cannot divide by {poly_str(divisor)}: it has not been proven nonzero")
    quotient = div_exact(poly, divisor)
    if quotient is None:
        raise Reject(f"the identity is not a multiple of {poly_str(divisor)}")
    branch.add([quotient])
    return _Outcome(source=poly, extra=divisor)


def _do_inj(state: State, branch: Branch, move: Inj) -> _Outcome:
    """Establish that f is injective (see ``injectivity_variable``)."""
    if "injective" in branch.props:
        raise Reject("f is already known to be injective")
    for poly in _candidates(state, branch, move.target):
        if injectivity_variable(branch, poly) is not None:
            branch.props.add("injective")
            return _Outcome(source=poly)
    raise Reject("no identity here shows that f is injective")


def _do_surj(state: State, branch: Branch, move: Surj) -> _Outcome:
    """Establish that f is surjective (see ``surjectivity_variable``)."""
    if "surjective" in branch.props:
        raise Reject("f is already known to be surjective")
    for poly in _candidates(state, branch, move.target):
        if surjectivity_variable(branch, poly) is not None:
            branch.props.add("surjective")
            return _Outcome(source=poly)
    raise Reject("no identity here shows that f is surjective")


def _do_cancel(state: State, branch: Branch, move: Cancel) -> _Outcome:
    """Cancel f from f(A) = f(B), which needs injectivity.

    Without injectivity f(A) = f(B) says nothing about A and B (think of a
    constant function), so the move is refused unless f has been proven
    injective in this branch.
    """
    if "injective" not in branch.props:
        raise Reject("cannot cancel f: injectivity has not been proven")
    for poly in _candidates(state, branch, move.target):
        for result in cancel_results(branch, poly):
            if not branch.known_zero(result):
                branch.add([result])
                return _Outcome(source=poly, instance=result)
    raise Reject("no identity of the form f(A) = f(B) gives anything new")


def _do_pre(state: State, branch: Branch, move: Pre) -> _Outcome:
    """Pick a preimage of a constant, which needs surjectivity.

    If f is surjective, every constant t equals f(a) for some a; the move
    names such an a (a fresh constant, never a variable: it is one fixed
    number, and it cannot be substituted for).
    """
    if "surjective" not in branch.props:
        raise Reject("cannot pick a preimage: surjectivity has not been proven")
    target = branch.norm(_term_poly(state, branch, move.term, ground=True))
    if len(branch.witnesses) >= MAX_WITNESSES:
        raise Reject("too many witnesses")
    for known, image in branch._rules.items():
        if known[0] == "f" and not atom_vars(known) and image == target:
            raise Reject(f"a preimage is already known: {poly_str(Poly.atom(known))} = {poly_str(target)}")
    name = next(n for n in WITNESS_NAMES if n not in branch.witnesses)
    branch.witnesses.append(name)
    branch.assumptions.append(("witness", name, target))
    branch.add([Poly.f(Poly.named(name)) - target])
    return _Outcome(witness=name, extra=target)


def _do_onto(state: State, branch: Branch, move: Onto) -> _Outcome:
    """Use surjectivity to replace f(y) by a free variable.

    Suppose f is surjective and, in an identity, the variable y occurs only
    inside f(y). Given any number t, pick y with f(y) = t; the identity for
    that y is the original one with f(y) replaced by t. So the identity with
    f(y) replaced by a variable holds for all values of that variable.

    The condition "y occurs only inside f(y)" matters: the y chosen depends
    on t, so y must not be visible anywhere else.
    """
    if "surjective" not in branch.props:
        raise Reject("cannot replace f(%s) by a variable: surjectivity has not been proven" % move.var)
    poly = _resolve(state, branch, move.target)
    name = move.var
    if name not in poly.variables():
        raise Reject(f"{name} does not occur in the identity")
    fresh = Poly.named("#t")
    replaced = poly.replace_atoms({("f", Poly.var(name).key): fresh})
    if name in replaced.variables():
        raise Reject(f"{name} occurs outside f({name}), so f({name}) cannot be replaced by a free variable")
    result = replaced.replace_atoms({("c", "#t"): Poly.var(name)})
    branch.add([result])
    return _Outcome(source=poly, instance=result)


def _do_cauchy(state: State, branch: Branch, move: Cauchy) -> _Outcome:
    """Cauchy's equation over Q, allowing a polynomial defect.

    Suppose f(u + v) = f(u) + f(v) + q(u, v) for all rational u, v, where q is
    a polynomial with constant coefficients. ``cauchy_form`` finds a
    polynomial p and a constant q0 with g = f - p satisfying
    g(u + v) = g(u) + g(v) + q0. Then h = g + q0 is additive, so h(n) = n*h(1)
    for integers n and h(m/n) = (m/n)*h(1): h is linear on Q. Unwinding,

        f(x) = p(x) + (f(1) - p(1) + q0)*x - q0.

    (With q = 0 this is the usual "additive on Q implies linear".)

    Over R this is FALSE without extra hypotheses (there are wild additive
    functions), so the move is refused unless the domain is Q.
    """
    if branch.domain != "Q":
        raise Reject("over R, additive does not imply linear (only over Q)")
    form = (ZERO, ZERO) if "additive" in branch.props and move.target is None else None
    source = None
    if form is None:
        for poly in _candidates(state, branch, move.target):
            form = cauchy_form(poly)
            if form is not None:
                source = poly
                break
    if form is None:
        raise Reject("no identity of the form f(x + y) = f(x) + f(y) + polynomial")
    p, constant = form
    one = Poly.f(Poly.const(1))
    explicit = Poly.f(X) - p - (one - p.subst({"x": Poly.const(1)}) + constant) * X + constant
    branch.add([explicit])
    return _Outcome(source=source, instance=explicit)


def _do_quadratic(state: State, branch: Branch, move: Quadratic) -> _Outcome:
    """The quadratic functional equation over Q.

    If f(u + v) + f(u - v) = 2f(u) + 2f(v) for all rational u, v, then:
    u = v = 0 gives f(0) = 0; u = 0 gives f(-v) = f(v); induction on n with
    (u, v) = (n*t, t) gives f(n*t) = n^2 f(t); hence f(t) = n^2 f(t/n) and
    f(m/n) = (m/n)^2 f(1). So f(x) = f(1)*x^2 on Q.

    Over R there are other solutions (built from a Hamel basis), so the move
    is refused unless the domain is Q.
    """
    if branch.domain != "Q":
        raise Reject("over R, the quadratic equation has non-polynomial solutions (lemma only over Q)")
    for poly in _candidates(state, branch, move.target):
        if is_quadratic_equation(poly):
            one = Poly.f(Poly.const(1))
            explicit = Poly.f(X) - one * X * X
            branch.add([explicit])
            return _Outcome(source=poly, instance=explicit)
    raise Reject("no identity of the form f(x + y) + f(x - y) = 2f(x) + 2f(y)")


def _do_conclude(state: State, branch: Branch, move: Conclude) -> _Outcome:
    """Read off f(x) = explicit expression and pin down the constants.

    The expression may involve unknown constants such as f(0). Whatever their
    values, f belongs to the family obtained by replacing them with free
    parameters. Substituting the family into the ORIGINAL equation and
    comparing coefficients tells us exactly which parameter values give
    solutions. So the solutions in this case are precisely the verified
    members of the family, and the case is closed.
    """
    for poly in _candidates(state, branch, move.target):
        expr = explicit_form(poly)
        if expr is None:
            continue
        family = _parametrise(expr)
        try:
            solutions = fit_candidate(state.problem.poly, family, branch.domain)
        except Unsupported as err:
            raise Reject(f"cannot pin down the constants: {err}") from None
        return _Outcome(branches=[], source=poly, candidate=expr, solutions=tuple(solutions), closed="concluded")
    raise Reject("no identity of the form f(x) = explicit expression")


_HANDLERS = {
    Subst: _do_subst,
    Split: _do_split,
    SplitNZ: _do_splitnz,
    Divide: _do_divide,
    Inj: _do_inj,
    Surj: _do_surj,
    Cancel: _do_cancel,
    Pre: _do_pre,
    Onto: _do_onto,
    Cauchy: _do_cauchy,
    Quadratic: _do_quadratic,
    Conclude: _do_conclude,
}


def apply(state: State, move: Move) -> State:
    """Apply one move to the current branch; raise ``Reject`` if it is not legal.

    A move that is legal but teaches nothing new is also rejected ("no new
    information"), which keeps proofs free of dead steps and prunes search.
    """
    if not state.branches:
        raise Reject("the proof is already complete")
    handler = _HANDLERS.get(type(move))
    if handler is None:
        raise Reject("unknown move")
    branch = state.current.copy()
    before = state.current
    before_sig = before.signature()
    try:
        outcome = handler(state, branch, move)
    except _Closed as closed:
        entry = LogEntry(move, case=before.case, closed="contradiction", reason=closed.reason)
        return State(state.problem, state.branches[1:], state.solutions, state.log + (entry,))
    log = dict(outcome.log)
    if outcome.branches is None:
        if branch.signature() == before_sig:
            raise Reject("no new information")
        old_rows = set(before.rows)
        log["new_rows"] = tuple(r for r in branch.rows if r not in old_rows)
        log["fresh_rows"] = tuple(r for r in log["new_rows"] if leading_mono(r) not in before._pivots)
        log["new_props"] = tuple(sorted(branch.props - before.props))
        branches = (branch,) + state.branches[1:]
    else:
        branches = tuple(outcome.branches) + state.branches[1:]
    solutions = state.solutions + tuple(log.get("solutions", ()))
    entry = LogEntry(move, case=before.case, **log)
    return State(state.problem, branches, solutions, state.log + (entry,))


# ---------------------------------------------------------------------------
# Checking whole proofs
# ---------------------------------------------------------------------------

@dataclass
class CheckResult:
    ok: bool                              # every move was accepted
    solved: bool                          # ... and no case is left open
    solutions: Optional[SolutionSet]      # the full solution set when solved
    error: Optional[str] = None
    step: Optional[int] = None            # index of the rejected move
    state: Optional[State] = None

    def __str__(self) -> str:
        if self.solved:
            return f"solved: {self.solutions}"
        if not self.ok and self.step is None:
            return f"not checked: {self.error}"
        if not self.ok:
            return f"rejected at move {self.step + 1}: {self.error}"
        return f"incomplete: {self.error}"


def check(problem: Problem, proof) -> CheckResult:
    """Replay a proof from the start. This is the definition of "solved".

    An equation over the size caps cannot be loaded (``initial_state`` raises
    ``Reject``); that is reported as a verdict like any refused move, with no
    move index and no state.
    """
    try:
        state = initial_state(problem)
    except Reject as reject:
        return CheckResult(False, False, None, f"{LOAD_REFUSED}: {reject.reason}", None, None)
    for index, move in enumerate(proof):
        try:
            state = apply(state, move)
        except Reject as reject:
            return CheckResult(False, False, None, f"{show_move(move)}: {reject.reason}", index, state)
    if state.branches:
        cases = len(state.branches)
        return CheckResult(True, False, None, f"{cases} case{'s' if cases != 1 else ''} still open", None, state)
    for expr in state.solutions:
        if not verify(problem.poly, expr):  # defence in depth: already verified at conclude
            return CheckResult(False, False, None, "internal error: a solution failed verification", None, state)
    return CheckResult(True, True, state.solution_set, None, None, state)


def verify_solution(problem: Problem, text: str) -> bool:
    """Does the formula ``f(x) = ...`` satisfy the problem's equation exactly?"""
    from .solutions import parse_solution

    return verify(problem.poly, parse_solution(text))
