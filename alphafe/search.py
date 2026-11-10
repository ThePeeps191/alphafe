"""Policy-guided proof search, independent of what the policy is.

A *proposer* suggests moves for a state (as token sequences with
log-probabilities). Two ways of using it:

``GreedySearch``  "no backtracking": take the proposer's best suggestion the
                  checker accepts and never undo it.
``BestFirstSearch``  keep a frontier of states, always expanding the one whose
                  path the proposer thinks most likely, within a budget of
                  checker calls.

Searches are written as small state machines (``request`` a node to expand,
``feed`` it proposals) so that many problems can be advanced together and the
network can be called on a whole batch of states at once (``run_searches``).
"""

from __future__ import annotations

import heapq
import itertools
import time
from typing import Optional

from . import terms as T
from .checker import Problem, Reject, State
from .env import SearchResult, confirm, start, step
from .tokenizer import StateView, decode_move, encode_state, sample_uniform


class Node:
    """A state reached during search, with the proof that reaches it."""

    __slots__ = ("state", "proof", "parent", "move_ids", "logp", "depth", "_view", "expansions", "fresh")

    def __init__(self, state: State, proof: list, parent: Optional["Node"], move_ids, logp: float, depth: int, fresh=()):
        self.state = state
        self.proof = proof
        self.parent = parent
        self.move_ids = move_ids      # the creative move (token ids) that led here from the parent
        self.logp = logp
        self.depth = depth
        self._view: Optional[StateView] = None
        self.expansions = 0
        self.fresh = fresh            # identities newly derived by that move (for hindsight examples)

    @property
    def view(self) -> StateView:
        if self._view is None:
            self._view = encode_state(self.state)
        return self._view


class _Search:
    """Shared bookkeeping for the two search modes."""

    source = ""

    def __init__(self, problem: Problem, budget: int, max_depth: int = 10):
        self.problem = problem
        self.budget = budget
        self.max_depth = max_depth
        self.calls = 0
        self.began = time.time()
        self.done = False
        self.solved_node: Optional[Node] = None
        self.solutions = None
        self.reason = ""
        self.nodes: list[Node] = []
        self.rejected = 0
        state, proof = start(problem)
        self.root = Node(state, proof, None, None, 0.0, 0)
        self.nodes.append(self.root)
        self.seen = {state.key()}
        if state.solved:
            self._finish_solved(self.root)

    def _finish_solved(self, node: Node) -> bool:
        solutions = confirm(self.problem, node.proof)
        if solutions is None:
            return False
        self.solved_node, self.solutions, self.done = node, solutions, True
        return True

    def _try(self, node: Node, ids: list, logp: float) -> Optional[Node]:
        """Send one proposed move to the checker. Returns the new node if it is accepted and new."""
        self.calls += 1
        try:
            move = decode_move(ids, node.view)
            new_state, applied = step(node.state, move)
        except (Reject, T.ParseError):
            self.rejected += 1
            return None
        entry = new_state.log[len(node.state.log)]
        child = Node(new_state, node.proof + applied, node, ids, node.logp + logp, node.depth + 1, entry.fresh_rows)
        if new_state.solved:
            if self._finish_solved(child):
                self.nodes.append(child)
                return child
            return None
        key = new_state.key()
        if key in self.seen:
            return None
        self.seen.add(key)
        self.nodes.append(child)
        return child

    def result(self) -> SearchResult:
        solved = self.solved_node is not None
        return SearchResult(
            solved=solved, proof=self.solved_node.proof if solved else [], solutions=self.solutions,
            checker_calls=self.calls, seconds=time.time() - self.began, nodes=len(self.nodes),
            reason="" if solved else (self.reason or "budget exhausted"), source=self.source,
        )

    def solution_path(self) -> list[Node]:
        """Nodes from the root to the solved node (empty if unsolved)."""
        path = []
        node = self.solved_node
        while node is not None:
            path.append(node)
            node = node.parent
        return path[::-1]


class GreedySearch(_Search):
    """No backtracking: commit to the first accepted proposal at every step."""

    source = "network-greedy"

    def __init__(self, problem: Problem, budget: int = 64, max_depth: int = 10, patience: int = 2):
        super().__init__(problem, budget, max_depth)
        self.current = self.root
        self.patience = patience          # how many empty-handed proposal rounds to tolerate per state
        self._misses = 0

    def request(self) -> Optional[Node]:
        return None if self.done else self.current

    def feed(self, proposals: list) -> None:
        node = self.current
        for ids, logp in sorted(proposals, key=lambda p: -p[1]):
            if self.calls >= self.budget:
                break
            child = self._try(node, ids, logp)
            if self.done:
                return
            if child is not None:
                self.current = child
                self._misses = 0
                if child.depth >= self.max_depth:
                    self.done, self.reason = True, "depth limit"
                return
        self._misses += 1
        if self.calls >= self.budget:
            self.done, self.reason = True, "budget exhausted"
        elif self._misses >= self.patience:
            self.done, self.reason = True, "no proposal was accepted"


class BestFirstSearch(_Search):
    """Expand the most promising state first, within a budget of checker calls.

    A state's priority is the log-probability of the moves leading to it. An
    expanded state goes back on the frontier with a penalty, so it can be
    revisited for fresh proposals once the alternatives look worse.
    """

    source = "network-search"

    def __init__(self, problem: Problem, budget: int = 256, max_depth: int = 10, revisit_penalty: float = 3.0):
        super().__init__(problem, budget, max_depth)
        self.revisit_penalty = revisit_penalty
        self._counter = itertools.count()
        self.frontier: list = []
        self._current: Optional[Node] = None
        if not self.done:
            self._push(self.root)

    def _push(self, node: Node) -> None:
        priority = node.logp - self.revisit_penalty * node.expansions
        heapq.heappush(self.frontier, (-priority, next(self._counter), node))

    def request(self) -> Optional[Node]:
        if self.done:
            return None
        if not self.frontier:
            self.done, self.reason = True, "frontier empty"
            return None
        _, _, self._current = heapq.heappop(self.frontier)
        return self._current

    def feed(self, proposals: list) -> None:
        node = self._current
        node.expansions += 1
        for ids, logp in sorted(proposals, key=lambda p: -p[1]):
            if self.calls >= self.budget:
                break
            child = self._try(node, ids, logp)
            if self.done:
                return
            if child is not None and child.depth < self.max_depth:
                self._push(child)
        if self.calls >= self.budget:
            self.done, self.reason = True, "budget exhausted"
            return
        if node.expansions < 6:
            self._push(node)


class UniformProposer:
    """The untrained reference policy: every grammar-allowed token equally likely."""

    def __init__(self, rng):
        self.rng = rng

    def propose(self, views: list, k: int) -> list:
        out = []
        for view in views:
            seen, proposals = set(), []
            for _ in range(k):
                ids, logp = sample_uniform(view, self.rng)
                if tuple(ids) not in seen:
                    seen.add(tuple(ids))
                    proposals.append((ids, logp))
            out.append(proposals)
        return out


def run_searches(searches: list, proposer, k: int) -> None:
    """Advance many searches together until all are done, batching the proposer's work."""
    while True:
        pending = []
        for search in searches:
            if not search.done:
                node = search.request()
                if node is not None:
                    pending.append((search, node))
        if not pending:
            return
        proposals = proposer.propose([node.view for _, node in pending], k)
        for (search, _), props in zip(pending, proposals):
            search.feed(props)
