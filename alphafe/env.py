"""The search environment shared by the brute-force baseline and the network.

On top of the checker it adds one convenience: after every proposed move the
*free moves* are applied until none applies. Free moves take no creative
input: establish injectivity or surjectivity, cancel f, use the Cauchy and
quadratic lemmas over Q, and conclude. This mirrors AlphaGeometry, where a symbolic engine runs all
routine deductions and the network only proposes the constructions (here:
substitutions, case splits, preimages).

Every free move is still an ordinary proof move: it is appended to the proof
and the final proof is re-checked from scratch by ``checker.check``.
"""

from __future__ import annotations

import functools
from dataclasses import dataclass, field
from typing import Optional

from . import terms as T
from .algebra import ZERO, Poly, TooLarge, atom_arg, atom_vars, poly_term
from .checker import LOAD_REFUSED, NORM_PASSES, WORK_TERMS, Problem, Reject, State, apply, check, initial_state
from .moves import Cancel, Cauchy, Conclude, Inj, Move, Quadratic, SqAdd, SqLin, Subst, Surj
from .solutions import SolutionSet

FREE_MOVES: tuple = (Conclude(), Cauchy(), Quadratic(), SqAdd(), SqLin(), Inj(), Surj(), Cancel())
MAX_FREE_STEPS = 40

# Routine substitutions (see ``routine_moves``). Each switch can be turned off
# to measure what it contributes; MAX_ROUTINE bounds the number applied after
# one proposed move.
ROUTINE = {"opening": True, "swap": True, "instances": True, "witness": True}
MAX_ROUTINE = 10
MAX_SITE_TERMS = 4      # arguments of f with more monomials than this are not used as substitution sites


def _opening_moves(problem: Problem) -> list[Move]:
    """The substitutions into P that nearly every solution starts with."""
    names = sorted(problem.poly.variables())
    zero = T.num(0)
    out: list[Move] = []
    if "x" in names and "y" in names:
        out.append(Subst("P", (("x", zero), ("y", zero))))
    for name in ("x", "y"):
        if name in names:
            out.append(Subst("P", ((name, zero),)))
    if "x" in names and "y" in names:
        out.append(Subst("P", (("y", T.Var("x")),)))
        out.append(Subst("P", (("y", T.Neg(T.Var("x"))),)))
    return out


@functools.lru_cache(maxsize=50_000)
def _f_atoms_of(poly: Poly) -> frozenset:
    return frozenset(atom for atom in poly.all_atoms() if atom[0] == "f")


def _f_atoms(polys) -> set:
    """Every f(...) that occurs in the polynomials, at any depth."""
    out: set = set()
    for poly in polys:
        out |= _f_atoms_of(poly)
    return out


@functools.lru_cache(maxsize=50_000)
def _instance(row: Poly, name: str, site: Poly) -> Optional[Poly]:
    """``row`` with the variable ``name`` replaced by ``site``, or None if that is over the checker's work limit.

    Cached: neighbouring states share most rows.
    """
    try:
        return row.subst({name: site}, WORK_TERMS)
    except TooLarge:
        return None


_VARIABLE = {name: Poly.var(name) for name in "xyz"}
_NORMAL: dict = {}


def _normal_instance(branch, row: Poly, name: str, site: Poly) -> Optional[Poly]:
    """``branch.norm`` of the instance of ``row`` at ``name := site``; None if the checker refuses to normalise it.

    Neighbouring states ask this for the same instances over and over, and
    the answer is the same whenever the rewriting meets the same rules. So
    it is kept together with what it depended on: the properties in force
    and, for every atom that was looked up, the rule it had (or that it had
    none). A stored answer is used only if all of that still holds, which
    makes it exactly what ``branch.norm`` would return.
    """
    key = (row, name, site)
    rules = branch._rules
    hit = _NORMAL.get(key)
    if hit is not None and hit[0] == branch.props:
        for atom, rule in hit[1]:
            if rules.get(atom) is not rule:
                break
        else:
            return hit[2]
    looked_up: dict = {}
    rewrite_atom = branch._rewrite_atom

    def fn(atom):
        if atom not in looked_up:
            looked_up[atom] = rules.get(atom)
        return rewrite_atom(atom)

    poly = _instance(row, name, site)
    result = None
    for _ in range(NORM_PASSES if poly is not None else 0):          # the loop of Branch.norm
        try:
            new = poly.rewrite(fn, limit=WORK_TERMS)
        except TooLarge:
            break
        if new is poly or new == poly:
            result = poly
            break
        poly = new
    if len(_NORMAL) > 200_000:
        _NORMAL.clear()
    _NORMAL[key] = (frozenset(branch.props), tuple(looked_up.items()), result)
    return result


def routine_moves(state: State, tried: set):
    """Substitutions that need no idea, as (key, move) pairs; ``tried`` holds the keys already used.

    * the swap ``sub P: x:=y, y:=x`` of a two-variable problem;
    * a named witness put into the original equation, one variable at a time;
    * closed instances: an identity in one variable v, taken at v := T where
      T is 0 or the argument of an f(...) already on the page, but only if
      the instance mentions no f(...) that is not on the page already (at
      T = 0, new variable-free ones are allowed). Without that condition the
      step feeds itself: f(f(x)) = 2f(x) + c at x := f(0), then at the new
      argument, and so on.

    Every one is an ordinary ``Subst``, checked by the checker and recorded
    in the proof like any other move. Knowledge in a case only grows, so
    applying them eagerly cannot lose a proof; it costs time and space.
    """
    branch = state.current
    rows = branch.rows
    names = sorted(state.problem.poly.variables())
    if ROUTINE["swap"] and len(names) == 2 and ("swap",) not in tried:
        yield ("swap",), Subst("P", ((names[0], T.Var(names[1])), (names[1], T.Var(names[0]))))
    if ROUTINE["witness"]:
        for witness in branch.witnesses:
            for name in names:
                key = ("witness", witness, name)
                if key not in tried:
                    yield key, Subst("P", ((name, T.Sym(witness)),))
    if not ROUTINE["instances"]:
        return
    present = _f_atoms(rows)
    sites = [ZERO]
    known_sites = {ZERO}
    for atom in sorted(present):
        arg = atom_arg(atom)
        if arg not in known_sites and len(arg.terms) <= MAX_SITE_TERMS:
            sites.append(arg)
            known_sites.add(arg)
    row_set = set(rows)
    for index, row in enumerate(rows):
        variables = row.variables()
        if len(variables) != 1:
            continue
        (name,) = variables
        if any(other < name and _instance(row, name, _VARIABLE[other]) in row_set for other in "xyz"):
            continue                      # a renamed copy of an identity that is handled through its first copy
        own = _VARIABLE[name] if name in _VARIABLE else Poly.var(name)
        for site in sites:
            key = (row, site)
            if key in tried or site == own:
                continue
            tried.add(key)
            instance = _normal_instance(branch, row, name, site)
            if instance is None or instance.is_zero():
                continue
            new_atoms = _f_atoms_of(instance) - present
            if new_atoms and not (site.is_zero() and not any(atom_vars(atom) for atom in new_atoms)):
                continue
            try:
                if branch.known_zero(instance):
                    continue              # already known: the checker would refuse it ("no new information")
            except Reject:
                pass                      # let the checker give its own verdict
            yield key, Subst(index, ((name, poly_term(site)),))


def close_free(state: State) -> tuple[State, list[Move]]:
    """Apply free moves until none is accepted. Returns the new state and the moves used."""
    applied: list[Move] = []
    progress = True
    while progress and state.branches and len(applied) < MAX_FREE_STEPS:
        progress = False
        for move in FREE_MOVES:
            try:
                state = apply(state, move)
            except Reject:
                continue
            applied.append(move)
            progress = True
            break
    return state, applied


def close(state: State) -> tuple[State, list[Move]]:
    """Apply the free moves and then routine substitutions until nothing more applies (or the cap is reached)."""
    state, applied = close_free(state)
    tried: set = set()
    count = 0
    progress = True
    while progress and state.branches and count < MAX_ROUTINE:
        progress = False
        for key, move in routine_moves(state, tried):
            tried.add(key)
            try:
                new_state = apply(state, move)
            except Reject:
                continue
            count += 1
            state, free = close_free(new_state)
            applied += [move] + free
            progress = True
            break
    return state, applied


def start(problem: Problem) -> tuple[State, list[Move]]:
    """Initial state with the free moves, the routine substitutions and the opening substitutions applied.

    Raises ``Reject`` if the checker cannot load the equation (it is over the
    size caps). Searches use ``try_start`` and report that as "not solved".
    """
    state, applied = close(initial_state(problem))
    if ROUTINE["opening"]:
        for move in _opening_moves(problem):
            if not state.branches:
                break
            try:
                state, more = step(state, move)
            except Reject:
                continue
            applied = applied + more
    return state, applied


def try_start(problem: Problem) -> tuple[Optional[State], list[Move], str]:
    """``start`` for search code: (state, moves, "") or (None, [], why the equation cannot be loaded)."""
    try:
        state, moves = start(problem)
    except Reject as reject:
        return None, [], f"{LOAD_REFUSED}: {reject.reason}"
    return state, moves, ""


def step(state: State, move: Move) -> tuple[State, list[Move]]:
    """Apply a proposed move, then the free moves. Raises ``Reject`` if the proposed move is refused."""
    state = apply(state, move)
    state, free = close(state)
    return state, [move] + free


@dataclass
class SearchResult:
    """Outcome of one solving attempt, whatever produced it."""

    solved: bool
    proof: list = field(default_factory=list)
    solutions: Optional[SolutionSet] = None
    checker_calls: int = 0          # proposed moves sent to the checker (accepted or not)
    seconds: float = 0.0
    nodes: int = 0                  # distinct states visited
    reason: str = ""                # why the attempt stopped when not solved
    source: str = ""                # "baseline", "network-greedy", "network-search"


def confirm(problem: Problem, proof: list) -> Optional[SolutionSet]:
    """Re-check a proof from scratch; return its solution set, or None if it is not a complete proof.

    Search code keeps its own states for speed, so before anything is called
    "solved" the proof is replayed through ``check`` with nothing shared.
    """
    result = check(problem, proof)
    return result.solutions if result.solved else None


def creative_moves(problem: Problem, proof: list) -> Optional[list]:
    """The moves of a proof that the environment did not add by itself, or None.

    A proof produced through ``start`` and ``step`` is the environment's own
    moves (free moves and routine substitutions) with the proposed moves in
    between. Replaying it tells them apart. None means the proof was not
    produced that way (a hand-written proof, say).
    """
    try:
        state, applied = start(problem)
    except Reject:
        return None
    if proof[:len(applied)] != applied:
        return None
    position, out = len(applied), []
    while position < len(proof):
        if state.solved:
            return None
        move = proof[position]
        try:
            state, applied = step(state, move)
        except Reject:
            return None
        if proof[position:position + len(applied)] != applied:
            return None
        out.append(move)
        position += len(applied)
    return out if state.solved else None


def quote_targets(problem: Problem, proof: list) -> list:
    """The same proof with ``R<n>`` targets replaced by the identity they point at, where that is possible.

    A numbered target means something else as soon as an earlier move is
    removed. A quoted identity (``sub [f(f(x)) = x]: ...``) does not. A row
    too large to be quoted keeps its number.
    """
    from dataclasses import replace

    from .algebra import poly_term
    from .moves import EqRef

    out = []
    try:
        state = initial_state(problem)
    except Reject:
        return list(proof)
    for move in proof:
        target = getattr(move, "target", None)
        chosen = move
        if isinstance(target, int) and not isinstance(target, bool) and state.branches and target < len(state.current.rows):
            quoted = replace(move, target=EqRef(poly_term(state.current.rows[target]), T.num(0)))
            try:
                if apply(state, quoted).key() == apply(state, move).key():
                    chosen = quoted
            except Reject:
                pass
        try:
            state = apply(state, chosen)
        except Reject:
            return list(proof)
        out.append(chosen)
    return out


def prune(problem: Problem, proof: list) -> list:
    """Drop every move a complete proof does not need.

    Moves are tried from the last to the first: a move can go if the rest is
    still a complete proof of the same answer, as judged by ``check``. This
    removes unused routine substitutions, unused free moves (an injectivity
    nothing relies on) and dead proposed moves alike. Passes repeat until
    nothing more goes. If the input is not a complete proof it is returned
    unchanged.
    """
    wanted = confirm(problem, proof)
    if wanted is None:
        return proof
    best = quote_targets(problem, proof)
    if confirm(problem, best) != wanted:
        best = list(proof)
    changed = True
    while changed:
        changed = False
        for index in range(len(best) - 1, -1, -1):
            shorter = best[:index] + best[index + 1:]
            if confirm(problem, shorter) == wanted:
                best = shorter
                changed = True
    return best


def minimise(problem: Problem, proof: list) -> list:
    """Shorten a complete proof, for display.

    First the proposed moves that are not needed are dropped: each is removed
    in turn, and if replaying the rest through the environment still solves
    the problem it was dead weight. Then ``prune`` removes every single move
    the result does not need, the environment's own moves included. The
    result is re-checked; if anything goes wrong the original proof is
    returned.
    """
    wanted = confirm(problem, proof)
    if wanted is None:
        return proof
    creative = creative_moves(problem, proof)

    def replay(moves):
        state, out = start(problem)
        out = list(out)
        try:
            for move in moves:
                if state.solved:
                    return None
                state, applied = step(state, move)
                out += applied
        except Reject:
            return None
        return out if state.solved else None

    best = proof
    if creative is not None:
        index = 0
        while index < len(creative):
            shorter = creative[:index] + creative[index + 1:]
            if replay(shorter) is not None:
                creative = shorter
            else:
                index += 1
        replayed = replay(creative)
        if replayed is not None and confirm(problem, replayed) == wanted and len(replayed) <= len(proof):
            best = replayed
    pruned = prune(problem, best)
    return pruned if confirm(problem, pruned) == wanted and len(pruned) <= len(proof) else proof
