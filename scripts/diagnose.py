"""Where does the network lose the thread on the problems it cannot solve?

    python scripts/diagnose.py checkpoints/best.pt [--suite seed|dev] [problem ids...]

For each hand-written proof of the suite, replay it and at every creative
move report (a) whether the network's move grammar can write that move at
all, and (b) the log-probability the network gives it in that state. The
last line gives the median, over the proofs, of the least likely step.

This is diagnosis only. The hand proofs are never used for training.
"""
import math
import sys

import torch

from alphafe.algebra import Poly, monic, to_poly
from alphafe.bench import BENCH_DIR, load_dev, load_seed
from alphafe.checker import Reject
from alphafe.env import FREE_MOVES, quote_targets, start, step
from alphafe.model import NeuralProposer, load_model
from alphafe.moves import EqRef, Onto, Split, Subst, parse_proof, show_move
from alphafe.tokenizer import encode_move, encode_state


def variants(move, state, view):
    """Every way the network could write this move in this state.

    The network can only point at the original equation P or at an identity
    shown in its view. A hand proof may quote an identity instead, or point at
    P when an identical row is also shown, or use the y-copy of a one-variable
    identity when only the x-copy is shown. All equivalent spellings count.
    """
    target = getattr(move, "target", None)
    if target is None:
        return [move]
    if target == "P":
        wanted = monic(state.problem.poly)
        out = [move]
    elif isinstance(target, EqRef):
        wanted = monic(to_poly(target.lhs) - to_poly(target.rhs))
        out = [Subst("P", move.bindings)] if isinstance(move, Subst) and wanted == monic(state.problem.poly) else []
    else:
        wanted = state.current.rows[target]
        out = []
    names = sorted(wanted.variables())
    renamings = [dict()]
    if len(names) == 1:
        renamings += [{names[0]: other} for other in "xyz" if other != names[0]]
    for renaming in renamings:
        image = wanted.subst({old: Poly.var(new) for old, new in renaming.items()})
        for index, row in enumerate(state.current.rows):
            if row != image or index not in view.label_of:
                continue
            if isinstance(move, Subst):
                out.append(Subst(index, tuple((renaming.get(n, n), t) for n, t in move.bindings)))
            elif isinstance(move, Split):
                out.append(Split(index))
            elif isinstance(move, Onto):
                out.append(Onto(index, renaming.get(move.var, move.var)))
    return out


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        sys.exit(__doc__)
    device = torch.device("cpu")
    model, _ = load_model(sys.argv[1], device)
    proposer = NeuralProposer(model, device)
    rest = sys.argv[2:]
    suite = "seed"
    if "--suite" in rest:
        at = rest.index("--suite")
        suite = rest[at + 1] if at + 1 < len(rest) else ""
        del rest[at: at + 2]
    if suite not in ("seed", "dev"):
        sys.exit("--suite takes seed or dev")
    wanted = set(rest)
    hardest = []
    for bench in (load_seed() if suite == "seed" else load_dev()):
        path = BENCH_DIR / suite / "proofs" / f"{bench.id}.proof"
        if not path.exists() or (wanted and bench.id not in wanted):
            continue
        state, _ = start(bench.problem)
        lines, worst, blocked, routine = [], 0.0, False, 0
        # Numbered targets in a hand proof count rows of the bare checker; the environment has more rows,
        # so the targets are quoted first.
        for move in quote_targets(bench.problem, parse_proof(path.read_text())):
            if state.solved:
                break
            if move in FREE_MOVES:
                continue            # the environment applies these by itself
            try:
                step(state, move)
            except Reject as reject:
                if reject.reason == "no new information":
                    routine += 1    # a routine substitution the environment has already made
                    continue
            view = encode_state(state)
            logps = []
            for candidate in variants(move, state, view):
                ids = encode_move(candidate, view)
                if ids is None:
                    continue
                try:
                    logps.append(proposer.logprob(view, ids))
                except ValueError:
                    pass
            if not logps:
                note = "NOT WRITABLE by the network (no shown identity to point at, or outside the move grammar)"
                blocked = True
            else:
                logp = math.log(sum(math.exp(v) for v in logps))
                note = f"log-prob {logp:7.2f}  (probability {math.exp(logp):.4f})"
                worst = min(worst, logp)
            lines.append(f"      {show_move(move):48s} {note}")
            try:
                state, _ = step(state, move)
            except Reject as reject:
                lines.append(f"      (replay stopped: {reject.reason})")
                break
        status = "blocked by the grammar" if blocked else f"least likely step {worst:.2f}"
        if lines:
            hardest.append(float("-inf") if blocked else worst)
        status += f"; {routine} of the hand proof's moves were already made by the environment"
        print(f"{bench.id}  {bench.problem.equation}   [{status}]")
        print("\n".join(lines))
    if hardest:
        ranked = sorted(hardest)
        print(f"{len(hardest)} proofs with at least one proposed move; least likely step: median {ranked[len(ranked) // 2]:.2f}, "
              f"above -5 in {sum(v > -5 for v in hardest)}, blocked by the grammar in {sum(v == float('-inf') for v in hardest)}")


if __name__ == "__main__":
    main()
