"""Brute-force proof search: breadth-first over moves with a fixed pool of substitution terms.

No learning and no heuristics beyond trying simple things first. States that
carry the same knowledge are merged. This is the control experiment the
network is compared against.
"""

from __future__ import annotations

import time
from collections import deque

from .. import terms as T
from ..algebra import leading_mono
from ..checker import Problem, Reject, State, _single_atom
from ..env import SearchResult, confirm, step, try_start
from ..moves import Move, Onto, Pre, Split, SplitNZ, Subst

# Terms tried for a single variable, simplest first.
SINGLE_POOL = [
    "0", "1", "-1", "x", "y", "-x", "-y", "x+y", "x-y", "y-x", "f(x)", "f(y)", "-f(x)", "-f(y)", "f(0)",
    "2x", "2y", "x/2", "y/2", "x+1", "y+1", "x-1", "y-1", "x-f(y)", "y-f(x)", "x+f(y)", "y+f(x)", "a",
]
# Terms tried when two variables are replaced at once.
PAIR_POOL = ["0", "1", "-1", "x", "y", "-x", "-y", "x+y", "x-y", "f(x)", "f(y)", "(x+y)/2", "(x-y)/2", "2x", "2y"]
SPLITNZ_POOL = ["f(0)", "f(1)"]
# Values whose preimage is named when f is surjective. The environment then puts the witness into P.
PRE_POOL = ["0", "1", "-1", "2"]
MAX_TARGET_ROWS = 6


def _pool(texts, names, witnesses) -> list:
    out = []
    for text in texts:
        term = T.parse(text)
        if T.term_vars(term) <= names and T.term_syms(term) <= witnesses:
            out.append(term)
    return out


# Iterative widening: (number of single terms, number of pair terms, depth limit).
# A narrow pool is searched deeply first, then wider pools more shallowly.
LADDER = ((5, 3, 6), (15, 9, 4), (len(SINGLE_POOL), len(PAIR_POOL), 8))


def candidate_moves(state: State, n_single: int = len(SINGLE_POOL), n_pair: int = len(PAIR_POOL)) -> list[Move]:
    """Every move the brute force is willing to try in this state, simplest first."""
    branch = state.current
    names = set(branch.names)
    witnesses = set(branch.witnesses)
    single = _pool(SINGLE_POOL[:n_single], names, witnesses)
    pair = _pool(PAIR_POOL[:n_pair], names, witnesses)
    moves: list[Move] = []

    # Case splits on facts about constants that are not already rewrite rules.
    for index, row in enumerate(branch.rows):
        if not row.variables() and _single_atom(leading_mono(row)) is None:
            moves.append(Split(index))

    targets = [("P", state.problem.poly)]
    for index, row in enumerate(branch.rows):
        if row.variables() and len(targets) <= MAX_TARGET_ROWS:
            targets.append((index, row))

    for target, poly in targets:
        own = sorted(poly.variables())
        for name in own:
            for term in single:
                if term != T.Var(name):
                    moves.append(Subst(target, ((name, term),)))
    for target, poly in targets:
        own = sorted(poly.variables())
        for i, first in enumerate(own):
            for second in own[i + 1:]:
                for t1 in pair:
                    for t2 in pair:
                        if t1 == T.Var(first) or t2 == T.Var(second):
                            continue  # that is a single substitution, tried above
                        moves.append(Subst(target, ((first, t1), (second, t2))))

    if "surjective" in branch.props:
        if not branch.witnesses:
            for text in PRE_POOL:
                moves.append(Pre(T.parse(text)))
        for index, row in enumerate(branch.rows):
            for name in sorted(row.variables()):
                moves.append(Onto(index, name))
    for text in SPLITNZ_POOL:
        moves.append(SplitNZ(T.parse(text)))
    return moves


def brute_force(problem: Problem, max_calls: int = 20000, max_seconds: float = 30.0,
                widening: bool = True, commit: bool = True) -> SearchResult:
    """Breadth-first search for a complete proof within a budget of checker calls and time.

    With ``widening`` the search runs the ``LADDER``: first a deep search with
    a tiny pool of substitution terms, then shallower searches with larger
    pools; each rung gets a share of the budget and the last rung gets
    whatever is left. Without it, one breadth-first search over the full pool.

    With ``commit`` the search restarts from any state in which a case has
    just been closed (see the comment below); this turns a proof with case
    splits into a sequence of shallow searches.
    """
    began = time.time()
    first_state, first_proof, refused = try_start(problem)
    if first_state is None:
        return SearchResult(solved=False, seconds=time.time() - began, reason=refused, source="baseline")
    calls = 0
    nodes = 0

    def finish(proof, reason):
        solutions = confirm(problem, proof) if proof is not None else None
        if proof is not None and solutions is None:
            reason = "proof failed re-checking"
        return SearchResult(
            solved=solutions is not None, proof=proof if solutions is not None else [], solutions=solutions,
            checker_calls=calls, seconds=time.time() - began, nodes=nodes, reason=reason, source="baseline",
        )

    if first_state.solved:
        return finish(first_proof, "")
    ladder = LADDER if widening else (LADDER[-1],)
    reason = "search space exhausted"
    # ``base`` is where every rung starts. It moves forward whenever a case is
    # closed. Among states from the same split the remaining cases do not
    # depend on how that case was closed; against states that never split it
    # is a heuristic that stays safe (each case knows at least what the
    # unsplit state knew) but may cost more moves.
    base_state, base_proof = first_state, first_proof
    for rung, (n_single, n_pair, max_depth) in enumerate(ladder):
        last = rung == len(ladder) - 1
        rung_limit = max_calls if last else calls + (max_calls - calls) // 3
        seen = {base_state.key()}
        queue = deque([(base_state, base_proof, 0)])
        stopped = False
        while queue and not stopped:
            state, proof, depth = queue.popleft()
            if depth >= max_depth:
                continue
            for move in candidate_moves(state, n_single, n_pair):
                if time.time() - began > max_seconds:
                    return finish(None, "time budget exhausted")
                if calls >= rung_limit:
                    stopped = True
                    break
                calls += 1
                try:
                    new_state, applied = step(state, move)
                except Reject:
                    continue
                new_proof = proof + applied
                if new_state.solved:
                    return finish(new_proof, "")
                if commit and len(new_state.branches) < len(state.branches):
                    base_state, base_proof = new_state, new_proof
                    seen = {new_state.key()}
                    queue = deque([(new_state, new_proof, 0)])
                    nodes += 1
                    break
                key = new_state.key()
                if key in seen:
                    continue
                seen.add(key)
                nodes += 1
                queue.append((new_state, new_proof, depth + 1))
        if stopped and last:
            reason = "checker-call budget exhausted"
    return finish(None, reason)
