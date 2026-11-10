"""Synthetic problem generator.

Recipe: pick a function F, pick a few random expressions involving f (the
*blocks*), combine them with small integer coefficients, and work out what
polynomial the combination equals when f = F. Writing "combination =
polynomial" gives a functional equation that F satisfies by construction.

The generator does not know the full solution set of what it produces (F is
just one solution, there may be others); a checked proof determines that.
Some generated problems are not solvable in the proof language at all.

Problems are sorted into curriculum *tiers* by structural size only (nesting
depth of f and term size), and split into train and held-out test sets by a
hash of their canonical form, so no problem is ever in both.
"""

from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations
from typing import Iterable, Optional

from . import terms as T
from .algebra import Poly, apply_function, monic, parse_poly, poly_term, to_poly
from .checker import Problem
from .env import start

# (weight, formula) for the planted solution F.
FUNCTIONS = [
    (20, "x"), (6, "-x"), (4, "x + 1"), (3, "x - 1"), (3, "x + 2"), (4, "2x"), (2, "3x"), (2, "x/2"), (2, "-2x"),
    (3, "2x + 1"), (2, "1 - x"), (2, "-x - 1"), (2, "3 - x"), (4, "0"), (2, "1"), (2, "2"), (5, "x^2"), (2, "x^2 + 1"),
    (2, "x^2 + x"), (1, "-x^2"), (1, "x^2 - x"), (1, "x^3"),
]

# Arguments of f, by level of complexity. Level 0 has no f inside.
ARGS_0 = [
    (10, "x"), (10, "y"), (8, "x + y"), (6, "x - y"), (3, "2x"), (2, "2y"), (4, "xy"), (2, "x^2"), (2, "y^2"),
    (2, "x + 2y"), (2, "2x + y"), (2, "-x"), (2, "-y"), (2, "x + 1"), (1, "y - 1"), (2, "0"), (1, "1"),
    (2, "x^2 - y^2"), (2, "x^2 + y"), (2, "xy + x"), (1, "x + y + 1"), (1, "y - x"), (1, "2x - y"),
]
ARGS_1 = [
    (6, "f(x)"), (6, "f(y)"), (8, "x + f(y)"), (6, "f(x) + y"), (4, "f(x) + f(y)"), (4, "x*f(y)"), (3, "y*f(x)"),
    (4, "x - f(y)"), (3, "f(x) - y"), (2, "x + f(x)"), (2, "f(x + y)"), (2, "2f(x)"), (2, "f(x) + 1"), (2, "x + y + f(y)"),
    (2, "f(x) - f(y)"), (2, "xy + f(x)"), (1, "x^2 + f(y)"), (2, "f(x)*f(y)"), (1, "x*f(x)"), (2, "f(y) - x"),
    (1, "2x + f(y)"), (1, "f(x) + 2y"),
]
# Multipliers placed in front of an f-block.
MULTIPLIERS = [(30, "1"), (4, "x"), (3, "y"), (1, "x + y"), (1, "x - y"), (1, "2")]
COEFFICIENTS = [1, 1, 1, 1, -1, -1, -1, 2, -2]

MAX_RESIDUAL_TERMS = 7
MAX_COEFFICIENT = 12
N_TIERS = 4


def _weighted(rng: random.Random, table):
    total = sum(w for w, _ in table)
    pick = rng.uniform(0, total)
    for weight, item in table:
        pick -= weight
        if pick <= 0:
            return item
    return table[-1][1]


@dataclass(frozen=True)
class Generated:
    equation: str
    domain: str
    planted: str          # the function used to build the equation (one solution, maybe not the only one)
    tier: int
    depth: int
    size: int
    key: str              # canonical hash (invariant under renaming variables and scaling)

    def problem(self) -> Problem:
        return Problem.parse(self.equation, self.domain, self.key[:10])

    @property
    def split(self) -> str:
        """'test' for roughly one problem in ten, decided by the canonical hash."""
        return "test" if int(self.key[:8], 16) % 10 == 0 else "train"


def canonical_key(poly: Poly) -> str:
    """Hash of an equation that ignores variable names, overall sign and scaling."""
    names = sorted(poly.variables())
    best = None
    for perm in permutations(names):
        renamed = poly.subst({old: Poly.var(new) for old, new in zip(names, perm)})
        text = repr(monic(renamed).key)
        if best is None or text < best:
            best = text
    return hashlib.sha256((best or "").encode()).hexdigest()


def tier_of(depth: int, size: int) -> int:
    """Curriculum tier from structure alone: shallow and small first."""
    if depth <= 1:
        return 1 if size <= 16 else 2
    if depth == 2:
        return 3 if size <= 24 else 4
    return 4


def _block(rng: random.Random, level: int) -> T.Term:
    """A random expression m * f(A) or f(A) * f(B)."""
    args = ARGS_1 if level >= 1 and rng.random() < 0.6 else ARGS_0
    block: T.Term = T.App(T.parse(_weighted(rng, args)))
    roll = rng.random()
    if roll < 0.12:
        block = T.Mul(block, T.App(T.parse(_weighted(rng, ARGS_0))))
    elif roll < 0.30:
        multiplier = _weighted(rng, MULTIPLIERS)
        if multiplier != "1":
            block = T.Mul(T.parse(multiplier), block)
    return block


def _side(pieces: list) -> T.Term:
    """Sum of (coefficient, term) pieces with positive coefficients."""
    if not pieces:
        return T.num(0)
    out: Optional[T.Term] = None
    for coef, term in pieces:
        piece = term if coef == 1 else T.Mul(T.num(coef), term)
        out = piece if out is None else T.Add(out, piece)
    return out


def generate_one(rng: random.Random, level: int) -> Optional[Generated]:
    """Try once to build a problem; returns None if the attempt is degenerate."""
    planted = _weighted(rng, FUNCTIONS)
    func = parse_poly(planted)
    n_blocks = rng.choice([2, 2, 3] if level <= 1 else [2, 3, 3, 4])
    blocks: list[T.Term] = []
    for _ in range(n_blocks):
        block = _block(rng, level)
        if all(to_poly(block) != to_poly(b) for b in blocks):
            blocks.append(block)
    if len(blocks) < 2 and rng.random() < 0.7:
        return None
    coefs = [rng.choice(COEFFICIENTS) for _ in blocks]
    coefs[0] = abs(coefs[0])
    combination = Poly()
    for coef, block in zip(coefs, blocks):
        combination = combination + to_poly(block) * coef
    residual = apply_function(combination, func)   # what the combination equals when f = F
    if len(residual.terms) > MAX_RESIDUAL_TERMS:
        return None
    if any(c.denominator != 1 or abs(c) > MAX_COEFFICIENT for c in residual.terms.values()):
        return None
    equation_poly = combination - residual
    if len(equation_poly.variables()) != 2:
        return None

    left = [(c, b) for c, b in zip(coefs, blocks) if c > 0]
    right = [(-c, b) for c, b in zip(coefs, blocks) if c < 0]
    lhs, rhs = _side(left), _side(right)
    if not residual.is_zero():
        rhs = poly_term(residual) if not right else T.Add(rhs, poly_term(residual))
        if isinstance(rhs, T.Add) and isinstance(rhs.right, T.Neg):
            rhs = T.Sub(rhs.left, rhs.right.arg)
    text = T.show_equation(lhs, rhs)
    domain = "Q" if rng.random() < 0.3 else "R"
    try:
        problem = Problem.parse(text, domain)
    except ValueError:
        return None
    if problem.poly != equation_poly:
        raise AssertionError("generator printed an equation that parses differently")
    depth = max(T.nesting_depth(lhs), T.nesting_depth(rhs))
    size = T.term_size(lhs) + T.term_size(rhs)
    if size > 40:
        return None
    state, _ = start(problem)
    if state.solved:
        return None  # trivial: the routine deductions alone finish it
    return Generated(text, domain, f"f(x) = {planted}", tier_of(depth, size), depth, size, canonical_key(problem.poly))


def generate(seed: int, per_tier: int, exclude: Iterable[str] = ()) -> dict:
    """Generate ``per_tier`` distinct problems for each tier.

    ``exclude`` is a set of canonical keys that must not be produced (the
    seed and real benchmarks, so that training never sees them).
    Returns {tier: [Generated, ...]}.
    """
    rng = random.Random(seed)
    seen = set(exclude)
    out: dict = {tier: [] for tier in range(1, N_TIERS + 1)}
    attempts = 0
    while any(len(v) < per_tier for v in out.values()) and attempts < per_tier * 4000:
        attempts += 1
        level = rng.choice([0, 0, 1, 1, 1])
        item = generate_one(rng, level)
        if item is None or item.key in seen or len(out[item.tier]) >= per_tier:
            continue
        seen.add(item.key)
        out[item.tier].append(item)
    return out


def benchmark_keys() -> set:
    """Canonical keys of every seed and real benchmark problem."""
    from .bench import load_real, load_seed

    return {canonical_key(b.problem.poly) for b in load_seed() + load_real()}
