"""Command line interface.

    alphafe solve "f(x+y) = f(x) + y" --domain R
    alphafe check "f(x+y) = f(x) + y" --domain R --proof proof.txt
    alphafe eval  --checkpoint checkpoints/best.pt
    alphafe train --run myrun --minutes 28
"""

from __future__ import annotations

import argparse
import pathlib
import pickle
import sys

from . import terms as T
from .bench import ROOT
from .checker import LOAD_REFUSED, Problem, check
from .env import SearchResult, minimise
from .moves import parse_proof, show_proof
from .render import render

DEFAULT_CHECKPOINT = ROOT / "checkpoints" / "best.pt"
# What loading a file that is not a checkpoint of this project can raise: torch reports most problems as
# pickle.UnpicklingError or RuntimeError, a truncated file gives EOFError, a foreign one KeyError or TypeError.
CHECKPOINT_ERRORS = (pickle.UnpicklingError, EOFError, KeyError, TypeError, RuntimeError)
EXIT_BAD_INPUT = 2      # distinct from 1, which means "no proof found" (solve) or "proof not accepted" (check)


def _load_network(checkpoint, device: str):
    """(model, device). Raises one of ``CHECKPOINT_ERRORS`` if the file is not a usable checkpoint."""
    from .model import load_model, pick_device

    dev = pick_device(device)
    model, _ = load_model(checkpoint, dev)
    return model, dev


def _solve_with_network(problem: Problem, model, dev, budget: int) -> SearchResult:
    from .model import DIVERSE, NeuralProposer
    from .search import BestFirstSearch, GreedySearch, run_searches

    greedy = GreedySearch(problem, budget=min(32, budget))
    run_searches([greedy], NeuralProposer(model, dev, temperature=DIVERSE), k=8)
    if greedy.solved_node is not None:
        return greedy.result()
    search = BestFirstSearch(problem, budget=budget)
    run_searches([search], NeuralProposer(model, dev, temperature=DIVERSE), k=8)
    result = search.result()
    result.checker_calls += greedy.calls
    return result


def cmd_solve(args) -> int:
    from .baseline.guesser import guess
    from .baseline.search import brute_force

    problem, renamed = Problem.parse(args.equation, args.domain).standard_names()
    if renamed:
        print("Variables renamed to x, y, z: " + ", ".join(f"{old} -> {new}" for old, new in renamed.items()) + ".")
    print(f"Problem: find all f: {problem.domain} -> {problem.domain} with {problem.equation}")
    print(f"Polynomial guess (not a proof): {guess(problem)}")
    result = None
    checkpoint = pathlib.Path(args.checkpoint)
    if not args.baseline:
        if checkpoint.exists():
            try:
                model, dev = _load_network(checkpoint, args.device)
            except CHECKPOINT_ERRORS as err:
                reason = str(err).strip().splitlines()[0][:200] if str(err).strip() else type(err).__name__
                print(f"Could not load {checkpoint} ({reason}); using the brute-force baseline.")
            else:
                result = _solve_with_network(problem, model, dev, args.budget)
                print(f"Network search: {'solved' if result.solved else 'not solved'} "
                      f"({result.checker_calls} checker calls, {result.seconds:.1f}s)")
        else:
            print(f"No checkpoint at {checkpoint}; using the brute-force baseline. (Train one with 'alphafe train', or download one: see README.)")
    if result is None or not result.solved:
        fallback = brute_force(problem, max_calls=args.baseline_budget, max_seconds=args.seconds)
        print(f"Brute-force baseline: {'solved' if fallback.solved else 'not solved'} "
              f"({fallback.checker_calls} checker calls, {fallback.seconds:.1f}s)")
        result = fallback
    if not result.solved:
        if result.reason.startswith(LOAD_REFUSED):
            print(f"\nNo proof found: {result.reason}. The equation is over the size limits that the checker")
            print("applies to every identity, so no search was run.")
            return 1
        print("\nNo proof found. The answer above is only a guess among polynomials of degree at most 2;")
        print("the problem may need moves outside the version-1 proof language.")
        return 1
    proof = minimise(problem, result.proof)
    dropped = len(result.proof) - len(proof)
    note = f" ({dropped} unneeded move{'s' if dropped != 1 else ''} removed)" if dropped else ""
    print(f"\nFound by: {result.source}{note}. Proof moves:\n{show_proof(proof)}\n")
    print(render(problem, proof))
    return 0


def cmd_check(args) -> int:
    problem = Problem.parse(args.equation, args.domain)
    text = sys.stdin.read() if args.proof == "-" else pathlib.Path(args.proof).read_text()
    proof = parse_proof(text)
    result = check(problem, proof)
    print(result)
    if result.ok and not args.quiet:
        print()
        print(render(problem, proof))
    return 0 if result.solved else 1


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "train":
        from .train import main as train_main

        train_main(argv[1:])
        return 0
    if argv and argv[0] == "eval":
        from .eval import main as eval_main

        eval_main(argv[1:])
        return 0

    parser = argparse.ArgumentParser(prog="alphafe", description="Solve easy olympiad functional equations with checked proofs.")
    sub = parser.add_subparsers(dest="command", required=True)

    solve = sub.add_parser("solve", help="find all solutions with a checked proof")
    solve.add_argument("equation", help='e.g. "f(x+y) = f(x) + y"')
    solve.add_argument("--domain", choices=["R", "Q"], default="R")
    solve.add_argument("--checkpoint", default=str(DEFAULT_CHECKPOINT))
    solve.add_argument("--budget", type=int, default=512, help="checker calls for the network search")
    solve.add_argument("--baseline", action="store_true", help="skip the network, use brute force only")
    solve.add_argument("--baseline-budget", type=int, default=20000)
    solve.add_argument("--seconds", type=float, default=60.0)
    solve.add_argument("--device", default="auto", choices=["auto", "cpu", "mps", "cuda"])
    solve.set_defaults(func=cmd_solve)

    chk = sub.add_parser("check", help="check a proof written in the move format")
    chk.add_argument("equation")
    chk.add_argument("--domain", choices=["R", "Q"], default="R")
    chk.add_argument("--proof", required=True, help="proof file, or - for standard input")
    chk.add_argument("--quiet", action="store_true", help="print the verdict only")
    chk.set_defaults(func=cmd_check)

    sub.add_parser("eval", help="three-mode evaluation (see 'alphafe eval --help')")
    sub.add_parser("train", help="self-play training (see 'alphafe train --help')")

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (T.ParseError, ValueError, OSError) as err:      # malformed equation or proof, unreadable file
        print(f"alphafe: error: {err}", file=sys.stderr)
        return EXIT_BAD_INPUT


if __name__ == "__main__":
    sys.exit(main())
