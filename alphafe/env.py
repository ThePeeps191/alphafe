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

from dataclasses import dataclass, field
from typing import Optional

from .checker import Problem, Reject, State, apply, check, initial_state
from .moves import Cancel, Cauchy, Conclude, Inj, Move, Quadratic, Surj
from .solutions import SolutionSet

FREE_MOVES: tuple = (Conclude(), Cauchy(), Quadratic(), Inj(), Surj(), Cancel())
MAX_FREE_STEPS = 40


def close(state: State) -> tuple[State, list[Move]]:
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


def start(problem: Problem) -> tuple[State, list[Move]]:
    """Initial state with the free moves already applied."""
    return close(initial_state(problem))


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
