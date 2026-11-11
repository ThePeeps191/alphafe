"""Replay a proof step by step and print the state after each move.

Usage: python scripts/play.py "<equation>" R|Q [proof-file | -]   (moves on stdin if '-')
Handy when writing proofs by hand.
"""
import sys

from alphafe.algebra import equation_str
from alphafe.checker import Problem, Reject, apply, initial_state
from alphafe.moves import parse_proof, show_move


def show(state):
    if not state.branches:
        print("   all cases closed. solutions:", state.solution_set)
        return
    b = state.current
    print(f"   [{len(state.branches)} open] case: {' / '.join(b.case) or '-'}  props: {sorted(b.props)}  nonzero: {[str(n) for n in b.nonzero]}")
    for i, row in enumerate(b.rows):
        print(f"     R{i + 1}: {equation_str(row)}")


def main():
    if len(sys.argv) < 3 or sys.argv[1] in ("-h", "--help"):
        sys.exit(__doc__)
    problem = Problem.parse(sys.argv[1], sys.argv[2])
    text = sys.stdin.read() if len(sys.argv) < 4 or sys.argv[3] == "-" else open(sys.argv[3]).read()
    state = initial_state(problem)
    print(problem)
    show(state)
    for move in parse_proof(text):
        print(">", show_move(move))
        try:
            state = apply(state, move)
        except Reject as r:
            print("   REJECTED:", r.reason)
            continue
        last = state.log[-1]
        if last.closed:
            print(f"   case closed ({last.closed}): {last.reason or [str(s) for s in last.solutions]}")
        for label, why in last.children:
            print(f"   case {label}" + (f": closed, {why}" if why else ""))
        show(state)


if __name__ == "__main__":
    main()
