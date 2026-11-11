"""Canonical polynomial arithmetic over *atoms*, with exact rational coefficients.

Every expression is stored as a polynomial

    sum of  coefficient * atom_1^e_1 * ... * atom_k^e_k

where an **atom** is one of

* ``('v', name)``  a universally quantified variable,
* ``('c', name)``  a named constant (a witness in a proof, a parameter in an answer),
* ``('f', key)``   the unknown function applied to another canonical polynomial
                   (``key`` is that polynomial's canonical key).

Two expressions are equal as formal expressions in f exactly when their
canonical polynomials are equal, so equality testing is a dictionary compare.
All coefficients are ``fractions.Fraction``; floats never appear.

This module is part of the trusted core: the checker relies on it. It is
written from scratch (no SymPy) because it sits in the search inner loop.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Callable, Iterable, Optional

from . import terms as T

Atom = tuple
Mono = tuple  # sorted tuple of (atom, exponent) pairs; () is the monomial 1

ONE = Fraction(1)


class FAtom(tuple):
    """The atom ``('f', key)``: an ordinary tuple that computes its hash once.

    Atoms sit inside the monomials that every dictionary of terms is keyed
    by, and Python hashes a plain nested tuple in full on every lookup. An
    FAtom equals, compares and hashes exactly like the plain tuple with the
    same content, so nothing depends on every atom being built here; equal
    FAtoms made by ``f_atom`` are also one object, which turns most
    comparisons into a pointer check. It also keeps its argument as a
    ``Poly`` (see ``atom_arg``).
    """

    def __new__(cls, key: tuple):
        self = tuple.__new__(cls, ("f", key))
        self._hash = tuple.__hash__(self)
        self._arg = None
        return self

    def __hash__(self) -> int:
        return self._hash

    def __reduce__(self):
        # The hash of a string differs between processes, so a stored hash must not travel.
        return (f_atom, (self[1],))


_ATOMS: dict = {}


def f_atom(key: tuple) -> FAtom:
    """The atom f(p) for the polynomial with canonical key ``key``."""
    atom = _ATOMS.get(key)
    if atom is None:
        if len(_ATOMS) > 500_000:
            _ATOMS.clear()          # atoms stay equal by content; only the sharing is lost
        atom = _ATOMS[key] = FAtom(key)
    return atom


def mono_mul(a: Mono, b: Mono) -> Mono:
    """Multiply two monomials (merge their atom/exponent lists)."""
    if not a:
        return b
    if not b:
        return a
    merged = dict(a)
    for atom, exp in b:
        merged[atom] = merged.get(atom, 0) + exp
    return tuple(sorted(merged.items()))


class Poly:
    """An immutable polynomial in atoms with Fraction coefficients.

    ``terms`` maps each monomial to its nonzero coefficient. Treat instances
    as immutable: every operation returns a new ``Poly``.
    """

    __slots__ = ("terms", "_key", "_hash", "_vars", "_lead", "_tops")

    def __init__(self, terms: Optional[dict] = None):
        self.terms: dict[Mono, Fraction] = terms if terms is not None else {}
        self._key = None
        self._hash = None
        self._vars = None
        self._lead = None       # (rank of the leading monomial, the monomial), see ``leading``
        self._tops = None

    # -- constructors -------------------------------------------------------

    @staticmethod
    def const(value) -> "Poly":
        value = Fraction(value)
        return Poly({(): value}) if value else Poly()

    @staticmethod
    def atom(atom: Atom) -> "Poly":
        return Poly({((atom, 1),): ONE})

    @staticmethod
    def var(name: str) -> "Poly":
        return Poly.atom(("v", name))

    @staticmethod
    def named(name: str) -> "Poly":
        return Poly.atom(("c", name))

    @staticmethod
    def f(arg: "Poly") -> "Poly":
        """The atom f(arg) as a polynomial."""
        atom = f_atom(arg.key)
        if atom._arg is None:
            atom._arg = arg
        return Poly.atom(atom)

    @staticmethod
    def from_key(key: tuple) -> "Poly":
        return Poly(dict(key))

    # -- identity -----------------------------------------------------------

    @property
    def key(self) -> tuple:
        """Canonical hashable form: the sorted tuple of (monomial, coefficient)."""
        if self._key is None:
            self._key = tuple(sorted(self.terms.items()))
        return self._key

    def __eq__(self, other) -> bool:
        if not isinstance(other, Poly):
            return NotImplemented
        return self.terms == other.terms

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self.key)
        return self._hash

    def __repr__(self) -> str:
        return f"Poly({poly_str(self)})"

    def __str__(self) -> str:
        return poly_str(self)

    # -- arithmetic ---------------------------------------------------------

    def __add__(self, other) -> "Poly":
        other = _coerce(other)
        if not other.terms:
            return self
        if not self.terms:
            return other
        out = dict(self.terms)
        for mono, coef in other.terms.items():
            value = out.get(mono)
            if value is None:
                out[mono] = coef
            else:
                value = value + coef
                if value:
                    out[mono] = value
                else:
                    del out[mono]
        return Poly(out)

    __radd__ = __add__

    def __neg__(self) -> "Poly":
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other) -> "Poly":
        other = _coerce(other)
        if not other.terms:
            return self
        out = dict(self.terms)
        for mono, coef in other.terms.items():
            value = out.get(mono)
            if value is None:
                out[mono] = -coef
            else:
                value = value - coef
                if value:
                    out[mono] = value
                else:
                    del out[mono]
        return Poly(out)

    def __rsub__(self, other) -> "Poly":
        return _coerce(other) - self

    def scale(self, factor) -> "Poly":
        factor = Fraction(factor)
        if not factor:
            return Poly()
        if factor == 1:
            return self
        return Poly({m: c * factor for m, c in self.terms.items()})

    def __mul__(self, other) -> "Poly":
        if not isinstance(other, Poly):
            return self.scale(other)
        if not self.terms or not other.terms:
            return Poly()
        if len(other.terms) == 1 and () in other.terms:
            return self.scale(other.terms[()])
        if len(self.terms) == 1 and () in self.terms:
            return other.scale(self.terms[()])
        out: dict[Mono, Fraction] = {}
        for m1, c1 in self.terms.items():
            for m2, c2 in other.terms.items():
                mono = mono_mul(m1, m2)
                value = out.get(mono)
                if value is None:
                    out[mono] = c1 * c2
                else:
                    value = value + c1 * c2
                    if value:
                        out[mono] = value
                    else:
                        del out[mono]
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, exp: int) -> "Poly":
        if exp < 0:
            raise ValueError("negative powers are not polynomials")
        result = Poly.const(1)
        for _ in range(exp):
            result = result * self
        return result

    # -- inspection ---------------------------------------------------------

    def is_zero(self) -> bool:
        return not self.terms

    def const_value(self) -> Optional[Fraction]:
        """The value if this is a rational constant, else ``None``."""
        if not self.terms:
            return Fraction(0)
        if len(self.terms) == 1 and () in self.terms:
            return self.terms[()]
        return None

    def top_atoms(self) -> frozenset:
        """Atoms that occur as factors of monomials (not inside f(...))."""
        tops = self._tops
        if tops is None:
            tops = self._tops = frozenset({atom for mono in self.terms for atom, _ in mono})
        return tops

    def all_atoms(self) -> set:
        """Atoms at every nesting level."""
        out: set = set()
        for atom in self.top_atoms():
            _collect_atoms(atom, out)
        return out

    def contains_atom(self, atom: Atom) -> bool:
        """Does ``atom`` occur anywhere, including inside f(...)?"""
        return any(_atom_contains(a, atom) for a in self.top_atoms())

    def variables(self) -> frozenset:
        """Names of all variables occurring at any depth."""
        if self._vars is None:
            names: set = set()
            for atom in self.top_atoms():
                names |= atom_vars(atom)
            self._vars = frozenset(names)
        return self._vars

    def is_ground(self) -> bool:
        return not self.variables()

    def coeffs_in(self, atom: Atom) -> dict:
        """View as a univariate polynomial in ``atom``: {exponent: coefficient Poly}.

        Only top-level occurrences count; ``atom`` nested inside f(...) stays
        inside the coefficients.
        """
        out: dict[int, dict] = {}
        for mono, coef in self.terms.items():
            exp = 0
            rest = mono
            for i, (a, e) in enumerate(mono):
                if a == atom:
                    exp = e
                    rest = mono[:i] + mono[i + 1:]
                    break
            out.setdefault(exp, {})[rest] = coef
        return {e: Poly(d) for e, d in out.items()}

    # -- rewriting ----------------------------------------------------------

    def rewrite(self, fn: Callable[[Atom], Optional["Poly"]], memo: Optional[dict] = None) -> "Poly":
        """Rewrite atoms bottom-up.

        ``fn(atom)`` returns a replacement polynomial or ``None`` to keep the
        atom. Arguments of f are rewritten first, then ``fn`` sees the rebuilt
        atom. The replacement itself is not rewritten again (single pass).
        Returns ``self`` (the same object) when nothing changed.
        """
        if memo is None:
            memo = {}
        changed = False
        replaced: dict = {}
        for atom in self.top_atoms():
            new = _rewrite_atom(atom, fn, memo)
            if new is not None:
                replaced[atom] = new
                changed = True
        if not changed:
            return self
        result = Poly()
        untouched: dict[Mono, Fraction] = {}
        for mono, coef in self.terms.items():
            if not any(atom in replaced for atom, _ in mono):
                untouched[mono] = coef
                continue
            # The atoms that stay form one monomial (still sorted); the replaced ones are multiplied in.
            product = Poly({tuple(pair for pair in mono if pair[0] not in replaced): coef})
            for atom, exp in mono:
                factor = replaced.get(atom)
                if factor is not None:
                    product = product * (factor if exp == 1 else factor ** exp)
            result = result + product
        return result + Poly(untouched)

    def subst(self, mapping: dict) -> "Poly":
        """Simultaneously replace variables: ``mapping`` is {name: Poly}.

        Substitution reaches inside f(...): f(x + y) with x := f(y) becomes
        f(f(y) + y).
        """
        if not mapping or not (self.variables() & mapping.keys()):
            return self

        def fn(atom):
            if atom[0] == "v":
                return mapping.get(atom[1])
            return None

        return self.rewrite(fn)

    def replace_atoms(self, mapping: dict) -> "Poly":
        """Replace whole atoms (at any depth): ``mapping`` is {atom: Poly}."""
        if not mapping:
            return self
        return self.rewrite(mapping.get)


ZERO = Poly()


def atom_arg(atom: Atom) -> Poly:
    """The argument p of the atom f(p). Shared between callers: treat it as immutable, like every ``Poly``."""
    if type(atom) is FAtom:
        arg = atom._arg
        if arg is None:
            arg = atom._arg = Poly(dict(atom[1]))
        return arg
    return Poly.from_key(atom[1])


def _coerce(value) -> Poly:
    return value if isinstance(value, Poly) else Poly.const(value)


def _collect_atoms(atom: Atom, out: set) -> None:
    if atom in out:
        return
    out.add(atom)
    if atom[0] == "f":
        for mono, _ in atom[1]:
            for inner, _ in mono:
                _collect_atoms(inner, out)


def _atom_contains(atom: Atom, target: Atom) -> bool:
    if atom == target:
        return True
    if atom[0] == "f":
        return any(_atom_contains(inner, target) for mono, _ in atom[1] for inner, _ in mono)
    return False


_VARS_CACHE: dict = {}


def atom_vars(atom: Atom) -> frozenset:
    """Variable names occurring in an atom (at any depth)."""
    kind = atom[0]
    if kind == "v":
        return frozenset((atom[1],))
    if kind == "c":
        return frozenset()
    cached = _VARS_CACHE.get(atom)
    if cached is None:
        names: set = set()
        for mono, _ in atom[1]:
            for inner, _ in mono:
                names |= atom_vars(inner)
        cached = frozenset(names)
        if len(_VARS_CACHE) > 200_000:
            _VARS_CACHE.clear()
        _VARS_CACHE[atom] = cached
    return cached


def _rewrite_atom(atom: Atom, fn, memo: dict) -> Optional[Poly]:
    """Rewrite one atom; ``None`` means unchanged."""
    if atom in memo:
        return memo[atom]
    result: Optional[Poly]
    if atom[0] == "f":
        arg = atom_arg(atom)
        new_arg = arg.rewrite(fn, memo)
        rebuilt = atom if new_arg is arg else f_atom(new_arg.key)
        result = fn(rebuilt)
        if result is None and rebuilt is not atom:
            result = Poly.atom(rebuilt)
    else:
        result = fn(atom)
    memo[atom] = result
    return result


# ---------------------------------------------------------------------------
# Size and ranking of atoms and monomials
# ---------------------------------------------------------------------------

_SIZE_CACHE: dict = {}
_DEPTH_CACHE: dict = {}


def atom_size(atom: Atom) -> int:
    """A structural size: variables 1, named constants 3, f(p) = 1 + size(p)."""
    kind = atom[0]
    if kind == "v":
        return 1
    if kind == "c":
        return 3
    cached = _SIZE_CACHE.get(atom)
    if cached is None:
        cached = 1 + key_size(atom[1])
        if len(_SIZE_CACHE) > 200_000:
            _SIZE_CACHE.clear()
        _SIZE_CACHE[atom] = cached
    return cached


def mono_size(mono: Mono) -> int:
    return sum(exp * atom_size(atom) for atom, exp in mono)


def key_size(key: tuple) -> int:
    """Size of a polynomial given by its key (a non-unit coefficient costs 1)."""
    total = 0
    for mono, coef in key:
        total += mono_size(mono) + (0 if coef == 1 else 1)
        if not mono:
            total += 1
    return total


def poly_size(poly: Poly) -> int:
    return key_size(poly.key)


def atom_depth(atom: Atom) -> int:
    """Nesting depth of f: variables and constants 0, f(x) 1, f(f(x)) 2."""
    if atom[0] != "f":
        return 0
    cached = _DEPTH_CACHE.get(atom)
    if cached is None:
        cached = 1 + max((atom_depth(a) for mono, _ in atom[1] for a, _ in mono), default=0)
        if len(_DEPTH_CACHE) > 200_000:
            _DEPTH_CACHE.clear()
        _DEPTH_CACHE[atom] = cached
    return cached


def poly_depth(poly: Poly) -> int:
    return max((atom_depth(a) for a in poly.top_atoms()), default=0)


def var_f_depth(mono: Mono) -> int:
    """Deepest nesting among the f-atoms of ``mono`` that contain a variable."""
    best = 0
    for atom, _ in mono:
        if atom[0] == "f" and atom_vars(atom):
            depth = atom_depth(atom)
            if depth > best:
                best = depth
    return best


def mono_rank(mono: Mono) -> tuple:
    """Total order on monomials used to pick the *leading* monomial of an identity.

    Monomials involving f of something with variables come last (largest), the
    more deeply nested the larger; ties are broken by structural size and then
    by the canonical tuple order. The leading monomial is the one linear
    elimination gets rid of first, so identities are solved for their most
    complicated term.
    """
    return (var_f_depth(mono), mono_size(mono), mono)


def leading(poly: Poly) -> tuple:
    """(rank, monomial) of the leading monomial of a nonzero polynomial, computed once per object."""
    lead = poly._lead
    if lead is None:
        mono = max(poly.terms, key=mono_rank)
        lead = poly._lead = (mono_rank(mono), mono)
    return lead


def leading_mono(poly: Poly) -> Mono:
    return leading(poly)[1]


def leading_rank(poly: Poly) -> tuple:
    """``mono_rank`` of the leading monomial: the key the checker sorts its identities by."""
    return leading(poly)[0]


def monic(poly: Poly) -> Poly:
    """Scale so the leading monomial has coefficient 1."""
    if not poly.terms:
        return poly
    lead = poly.terms[leading_mono(poly)]
    return poly if lead == 1 else poly.scale(1 / lead)


def has_var_f(poly: Poly) -> bool:
    """Does the polynomial contain f applied to something with a variable?"""
    return any(atom[0] == "f" and atom_vars(atom) for atom in poly.top_atoms())


# ---------------------------------------------------------------------------
# Coefficient extraction, exact division, factoring hints
# ---------------------------------------------------------------------------

def split_by_vars(poly: Poly) -> dict:
    """Group monomials by their variable part: {variable-monomial: coefficient Poly}.

    Only meaningful when no f-atom contains a variable; then the polynomial is
    an ordinary polynomial in the variables whose coefficients are constants.
    """
    out: dict[Mono, dict] = {}
    for mono, coef in poly.terms.items():
        var_part = tuple(pair for pair in mono if pair[0][0] == "v")
        rest = tuple(pair for pair in mono if pair[0][0] != "v")
        out.setdefault(var_part, {})[rest] = coef
    return {vp: Poly(d) for vp, d in out.items()}


def div_exact(p: Poly, q: Poly) -> Optional[Poly]:
    """Return p / q if q divides p exactly as polynomials in the atoms, else None.

    Atoms are treated as independent indeterminates. The algorithm is long
    division in one atom of q, recursing on the leading coefficients.
    """
    if not q.terms:
        raise ZeroDivisionError("division by the zero polynomial")
    if not p.terms:
        return ZERO
    c = q.const_value()
    if c is not None:
        return p.scale(1 / c)
    main = max(q.top_atoms())
    q_coeffs = q.coeffs_in(main)
    dq = max(q_coeffs)
    lq = q_coeffs[dq]
    main_poly = Poly.atom(main)
    quotient = ZERO
    remainder = p
    while remainder.terms:
        r_coeffs = remainder.coeffs_in(main)
        dr = max(r_coeffs)
        if dr < dq:
            return None
        lead = div_exact(r_coeffs[dr], lq)
        if lead is None:
            return None
        term = lead * (main_poly ** (dr - dq))
        quotient = quotient + term
        remainder = remainder - term * q
    return quotient


def univariate_coeffs(poly: Poly) -> Optional[tuple]:
    """If ``poly`` is a polynomial in a single top-level atom with rational
    coefficients, return (atom, [c0, c1, ..., cd]); otherwise None."""
    atoms = poly.top_atoms()
    if len(atoms) != 1:
        return None
    (atom,) = atoms
    degree = max(mono[0][1] if mono else 0 for mono in poly.terms)
    coeffs = [Fraction(0)] * (degree + 1)
    for mono, coef in poly.terms.items():
        coeffs[mono[0][1] if mono else 0] = coef
    return atom, coeffs


def _divisors(n: int) -> list[int]:
    n = abs(n)
    out = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            out.append(i)
            if i != n // i:
                out.append(n // i)
        i += 1
    return out


class Unsupported(Exception):
    """The exact machinery cannot handle this case (it is *not* a refutation)."""


def rational_roots(coeffs: list) -> list:
    """All rational roots of c0 + c1 t + ... + cd t^d (rational root theorem).

    Every rational root p/q in lowest terms has p | (lowest nonzero
    coefficient) and q | (leading coefficient) once denominators are cleared.
    The candidates are tested exactly, so the returned list is complete.
    """
    coeffs = list(coeffs)
    while coeffs and coeffs[-1] == 0:
        coeffs.pop()
    if not coeffs:
        raise ValueError("the zero polynomial has every number as a root")
    roots = []
    if coeffs[0] == 0:
        roots.append(Fraction(0))
        while coeffs[0] == 0:
            coeffs.pop(0)
    if len(coeffs) == 1:
        return roots
    lcm = 1
    for c in coeffs:
        d = c.denominator
        g = _gcd(lcm, d)
        lcm = lcm * d // g
    ints = [int(c * lcm) for c in coeffs]
    if abs(ints[0]) > 10**7 or abs(ints[-1]) > 10**7:
        raise Unsupported("coefficients too large for the rational root search")
    seen = set()
    for p in _divisors(ints[0]):
        for q in _divisors(ints[-1]):
            for cand in (Fraction(p, q), Fraction(-p, q)):
                if cand in seen:
                    continue
                seen.add(cand)
                value = Fraction(0)
                for c in reversed(ints):
                    value = value * cand + c
                if value == 0:
                    roots.append(cand)
    return sorted(roots)


def _gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


def has_no_root(coeffs: list, domain: str) -> bool:
    """True only when c0 + c1 t + ... has provably no root in the domain.

    Over Q: no rational root (the rational root test is complete). Over R we
    additionally need the polynomial to have no irrational real root, which we
    only certify in two easy cases: a quadratic with negative discriminant, or
    a polynomial with only even powers whose coefficients all share one sign.
    """
    coeffs = list(coeffs)
    while coeffs and coeffs[-1] == 0:
        coeffs.pop()
    if len(coeffs) <= 1:
        return bool(coeffs)  # nonzero constant: no root; zero polynomial: roots
    try:
        if rational_roots(coeffs):
            return False
    except Unsupported:
        return False
    if domain == "Q":
        return True
    if len(coeffs) == 3:
        c, b, a = coeffs
        return b * b - 4 * a * c < 0
    if all(c == 0 for c in coeffs[1::2]):
        signs = {c > 0 for c in coeffs[0::2] if c != 0}
        return len(signs) == 1 and coeffs[0] != 0
    return False


def unique_root(coeffs: list, domain: str):
    """The root of c0 + c1 t + ... if it provably has exactly one root in the domain, else None.

    That is: exactly one distinct rational root, and what remains after
    dividing it out (with multiplicity) has no root in the domain.
    """
    coeffs = list(coeffs)
    while coeffs and coeffs[-1] == 0:
        coeffs.pop()
    if len(coeffs) < 2:
        return None
    try:
        roots = rational_roots(coeffs)
    except Unsupported:
        return None
    if len(roots) != 1:
        return None
    root = roots[0]
    while len(coeffs) > 1 and sum(c * root**i for i, c in enumerate(coeffs)) == 0:
        quotient = [Fraction(0)] * (len(coeffs) - 1)
        carry = Fraction(0)
        for i in range(len(coeffs) - 1, 0, -1):
            carry = coeffs[i] + carry * root
            quotient[i - 1] = carry
        coeffs = quotient
    if len(coeffs) > 1 and not has_no_root(coeffs, domain):
        return None
    return root


def factor_hint(poly: Poly) -> list:
    """Try to factor ``poly`` into [(factor, multiplicity), ...].

    This is an *untrusted helper*: callers must re-multiply the factors and
    compare with the original. It finds common atom factors, rational roots of
    univariate polynomials, and splits of the form u*(A + w/u).
    """
    factors: list[tuple[Poly, int]] = []
    if not poly.terms:
        return factors
    # Common atom factors.
    common: Optional[dict] = None
    for mono in poly.terms:
        exps = dict(mono)
        if common is None:
            common = exps
        else:
            common = {a: min(e, exps[a]) for a, e in common.items() if a in exps}
        if not common:
            break
    rest = poly
    if common:
        for atom, exp in sorted(common.items()):
            factors.append((Poly.atom(atom), exp))
            divisor = Poly.atom(atom) ** exp
            rest = div_exact(rest, divisor)
    factors.extend(_factor_rest(rest, depth=0))
    return factors


def _factor_rest(poly: Poly, depth: int) -> list:
    if poly.const_value() is not None:
        return []
    uni = univariate_coeffs(poly)
    if uni is not None:
        atom, coeffs = uni
        try:
            roots = rational_roots(coeffs)
        except Unsupported:
            return [(poly, 1)]
        out = []
        rest = poly
        a = Poly.atom(atom)
        for root in roots:
            linear = a - root
            mult = 0
            while True:
                q = div_exact(rest, linear)
                if q is None:
                    break
                rest = q
                mult += 1
            if mult:
                out.append((linear, mult))
        if rest.const_value() is None:
            out.append((monic(rest), 1))
        return out
    if depth < 4:
        for atom in sorted(poly.top_atoms()):
            cs = poly.coeffs_in(atom)
            if set(cs) == {0, 1} and cs[1].const_value() is None:
                q = div_exact(cs[0], cs[1])
                if q is not None:
                    return _factor_rest(cs[1], depth + 1) + [(monic(Poly.atom(atom) + q), 1)]
    return [(poly, 1)]


# ---------------------------------------------------------------------------
# Conversion between terms and polynomials, printing
# ---------------------------------------------------------------------------

def to_poly(term: T.Term) -> Poly:
    """Canonicalise a term."""
    if isinstance(term, T.Num):
        return Poly.const(term.value)
    if isinstance(term, T.Var):
        return Poly.var(term.name)
    if isinstance(term, T.Sym):
        return Poly.named(term.name)
    if isinstance(term, T.App):
        return Poly.f(to_poly(term.arg))
    if isinstance(term, T.Add):
        return to_poly(term.left) + to_poly(term.right)
    if isinstance(term, T.Sub):
        return to_poly(term.left) - to_poly(term.right)
    if isinstance(term, T.Mul):
        return to_poly(term.left) * to_poly(term.right)
    if isinstance(term, T.Neg):
        return -to_poly(term.arg)
    if isinstance(term, T.Pow):
        return to_poly(term.base) ** term.exp
    raise TypeError(f"not a term: {term!r}")


def parse_poly(text: str) -> Poly:
    return to_poly(T.parse(text))


def equation_poly(text: str) -> Poly:
    """Parse ``lhs = rhs`` and return the canonical polynomial lhs - rhs."""
    lhs, rhs = T.parse_equation(text)
    return to_poly(lhs) - to_poly(rhs)


def atom_term(atom: Atom) -> T.Term:
    kind = atom[0]
    if kind == "v":
        return T.Var(atom[1])
    if kind == "c":
        return T.Sym(atom[1])
    return T.App(poly_term(atom_arg(atom)))


def _mono_term(mono: Mono, coef: Fraction) -> T.Term:
    """Term for |coef| * mono (the sign is handled by the caller)."""
    coef = abs(coef)
    factors: list[T.Term] = []
    # constants first, then variables, then f of variables: reads as 2f(1)xyf(x)
    def order(pair):
        atom = pair[0]
        if atom[0] == "v":
            return (1, atom)
        return (2 if atom_vars(atom) else 0, atom)

    for atom, exp in sorted(mono, key=order):
        base = atom_term(atom)
        factors.append(base if exp == 1 else T.Pow(base, exp))
    if not factors:
        return T.Num(coef)
    if coef != 1 and coef.numerator != 1:
        factors.insert(0, T.Num(coef))  # 2f(1)x
    body = factors[0]
    for factor in factors[1:]:
        body = T.Mul(body, factor)
    if coef != 1 and coef.numerator == 1:
        return T.Mul(body, T.Num(coef))  # printed as body/n
    return body


def _display_rank(mono: Mono) -> tuple:
    """Display order: f of variables first, then by degree in the variables
    (x^2 before x before constants), then by size; ties alphabetical."""
    var_degree = sum(exp for atom, exp in mono if atom[0] == "v")
    return (-var_f_depth(mono), -var_degree, -mono_size(mono), mono)


def poly_term(poly: Poly) -> T.Term:
    """A readable term for a canonical polynomial (largest monomials first)."""
    if not poly.terms:
        return T.Num(Fraction(0))
    # Most complicated monomials first; ties in alphabetical order.
    monos = sorted(poly.terms, key=_display_rank)
    # Lead with a positive monomial when there is one: "x - f(x)" not "-f(x) + x".
    first = next((m for m in monos if poly.terms[m] > 0), None)
    if first is not None:
        monos.remove(first)
        result: T.Term = _mono_term(first, poly.terms[first])
    else:
        first = monos.pop(0)
        result = T.Neg(_mono_term(first, poly.terms[first]))
    for mono in monos:
        coef = poly.terms[mono]
        piece = _mono_term(mono, coef)
        result = T.Add(result, piece) if coef > 0 else T.Sub(result, piece)
    return result


def poly_str(poly: Poly) -> str:
    return T.show(poly_term(poly))


def equation_sides(poly: Poly) -> tuple[Poly, Poly]:
    """Split ``poly = 0`` into a readable ``lhs = rhs``.

    The leading monomial goes on the left with a positive coefficient and
    everything else moves to the right: f(x + y) - f(x) - y = 0 is shown as
    f(x + y) = f(x) + y.
    """
    if not poly.terms:
        return ZERO, ZERO
    lead = leading_mono(poly)
    coef = poly.terms[lead]
    lhs = Poly({lead: abs(coef)})
    rhs = lhs - (poly if coef > 0 else -poly)
    return lhs, rhs


def equation_str(poly: Poly) -> str:
    lhs, rhs = equation_sides(poly)
    return f"{poly_str(lhs)} = {poly_str(rhs)}"


# ---------------------------------------------------------------------------
# Evaluation (used by tests and the model-check fuzzer, never by the checker)
# ---------------------------------------------------------------------------

def evaluate(poly: Poly, func: Callable[[Fraction], Fraction], values: dict) -> Fraction:
    """Evaluate exactly, given a concrete function for f and values for the
    variables and named constants (``values`` maps names to Fractions)."""
    total = Fraction(0)
    for mono, coef in poly.terms.items():
        product = coef
        for atom, exp in mono:
            product *= _eval_atom(atom, func, values) ** exp
        total += product
    return total


def _eval_atom(atom: Atom, func, values: dict) -> Fraction:
    if atom[0] == "f":
        return Fraction(func(evaluate(atom_arg(atom), func, values)))
    return Fraction(values[atom[1]])


def apply_function(poly: Poly, expr: Poly, var: str = "x") -> Poly:
    """Replace every f(A) by ``expr`` with ``var`` := A, innermost first.

    ``expr`` describes a candidate solution f(var) = expr and must not itself
    contain f. The result contains no f at all, so "the candidate satisfies
    the equation" becomes "the result is the zero polynomial".
    """

    def fn(atom):
        if atom[0] == "f":
            return expr.subst({var: atom_arg(atom)})
        return None

    return poly.rewrite(fn)
