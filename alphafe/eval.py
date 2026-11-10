"""Evaluation: run solvers over benchmarks and tabulate solve rate, checker calls and time."""

from __future__ import annotations

import json
import multiprocessing as mp
import pathlib
import time
from dataclasses import asdict, dataclass
from typing import Callable, Optional

from .bench import ROOT, BenchProblem, canary
from .env import SearchResult
from .moves import show_proof

RESULTS_DIR = ROOT / "results"


@dataclass
class Row:
    """One problem attempted by one solver."""

    id: str
    equation: str
    domain: str
    mohs: Optional[int]
    solved: bool
    checker_calls: int
    seconds: float
    proof_len: int
    answer: str
    reason: str
    proof: str = ""


def score(bench: BenchProblem, result: SearchResult) -> Row:
    """Turn a search result into a table row; raises ``AnswerMismatch`` on a wrong accepted answer."""
    if result.solved:
        canary(bench, result.solutions)
    return Row(
        id=bench.id, equation=bench.problem.equation, domain=bench.problem.domain, mohs=bench.mohs,
        solved=result.solved, checker_calls=result.checker_calls, seconds=round(result.seconds, 3),
        proof_len=len(result.proof), answer=str(result.solutions) if result.solved else "",
        reason=result.reason, proof=show_proof(result.proof) if result.solved else "",
    )


def _baseline_job(args) -> SearchResult:
    from .baseline.search import brute_force

    problem, max_calls, max_seconds, widening = args
    return brute_force(problem, max_calls=max_calls, max_seconds=max_seconds, widening=widening)


def run_baseline(benches: list[BenchProblem], max_calls: int, max_seconds: float, workers: int = 8,
                 widening: bool = True) -> list[Row]:
    """Brute-force baseline over a list of problems, in parallel."""
    jobs = [(b.problem, max_calls, max_seconds, widening) for b in benches]
    if workers <= 1:
        results = [_baseline_job(j) for j in jobs]
    else:
        with mp.get_context("spawn").Pool(workers) as pool:
            results = pool.map(_baseline_job, jobs)
    return [score(b, r) for b, r in zip(benches, results)]


def summary(rows: list[Row]) -> dict:
    solved = [r for r in rows if r.solved]
    n = len(rows)
    return {
        "problems": n,
        "solved": len(solved),
        "rate": round(len(solved) / n, 4) if n else 0.0,
        "mean_calls_solved": round(sum(r.checker_calls for r in solved) / len(solved), 1) if solved else None,
        "median_calls_solved": sorted(r.checker_calls for r in solved)[len(solved) // 2] if solved else None,
        "mean_seconds": round(sum(r.seconds for r in rows) / n, 3) if n else 0.0,
    }


def by_mohs(rows: list[Row]) -> dict:
    out: dict = {}
    for r in rows:
        key = "?" if r.mohs is None else f"{r.mohs}M"
        cell = out.setdefault(key, [0, 0])
        cell[0] += r.solved
        cell[1] += 1
    return dict(sorted(out.items(), key=lambda kv: (kv[0] == "?", int(kv[0][:-1]) if kv[0] != "?" else 0)))


def save(name: str, rows: list[Row], config: dict) -> pathlib.Path:
    """Write a run to results/<name>.json (small, committed; the source for RESULTS.md tables)."""
    RESULTS_DIR.mkdir(exist_ok=True)
    path = RESULTS_DIR / f"{name}.json"
    payload = {"name": name, "config": config, "summary": summary(rows), "by_mohs": by_mohs(rows),
               "rows": [asdict(r) for r in rows]}
    path.write_text(json.dumps(payload, indent=1) + "\n")
    return path


def markdown_summary(runs: dict) -> str:
    """A markdown table comparing runs: {label: rows}."""
    lines = ["| solver | solved | rate | mean checker calls (solved) | median calls (solved) | mean time per problem |",
             "|---|---|---|---|---|---|"]
    for label, rows in runs.items():
        s = summary(rows)
        lines.append(f"| {label} | {s['solved']}/{s['problems']} | {100 * s['rate']:.1f}% | "
                     f"{s['mean_calls_solved']} | {s['median_calls_solved']} | {s['mean_seconds']}s |")
    return "\n".join(lines)


def markdown_by_mohs(runs: dict) -> str:
    keys: list = []
    tables = {label: by_mohs(rows) for label, rows in runs.items()}
    for table in tables.values():
        for key in table:
            if key not in keys:
                keys.append(key)
    lines = ["| solver | " + " | ".join(keys) + " |", "|---|" + "---|" * len(keys)]
    for label, table in tables.items():
        cells = [f"{table[k][0]}/{table[k][1]}" if k in table else "-" for k in keys]
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Network modes and the full three-mode evaluation
# ---------------------------------------------------------------------------

GREEDY_BUDGET = 32      # "network, no backtracking": checker calls allowed
SEARCH_BUDGET = 128     # "network, small search budget"
PROPOSALS = 8           # proposals requested per expanded state


def run_policy(benches: list[BenchProblem], proposer, mode: str, budget: int, k: int = PROPOSALS,
               value_weight: float = 0.0) -> list[Row]:
    """Run a proposer (network or uniform) over problems. mode: 'greedy' or 'search'."""
    from .search import BestFirstSearch, GreedySearch, run_searches

    if mode == "greedy":
        searches = [GreedySearch(b.problem, budget=budget) for b in benches]
    else:
        searches = [BestFirstSearch(b.problem, budget=budget, value_weight=value_weight) for b in benches]
    began = time.time()
    run_searches(searches, proposer, k)
    elapsed = (time.time() - began) / max(1, len(benches))
    rows = []
    for bench, search in zip(benches, searches):
        result = search.result()
        result.seconds = elapsed      # searches run interleaved; report the average share
        rows.append(score(bench, result))
    return rows


HELDOUT_FILE = "heldout.jsonl"


def synthetic_heldout(limit: int = 200) -> dict:
    """Held-out synthetic test problems by tier, from the frozen file
    benchmarks/synthetic/heldout.jsonl (written once by scripts/freeze_heldout.py).
    Their answers are unknown, so "solved" means a checked proof was found."""
    from .bench import BENCH_DIR
    from .checker import Problem

    out: dict = {}
    for line in (BENCH_DIR / "synthetic" / HELDOUT_FILE).read_text().splitlines():
        rec = json.loads(line)
        bucket = out.setdefault(rec["tier"], [])
        if len(bucket) < limit:
            problem = Problem.parse(rec["equation"], rec["domain"], rec["id"])
            bucket.append(BenchProblem(rec["id"], problem, None, None, rec["source"], rec))
    return dict(sorted(out.items()))


def common_calls(first: list[Row], second: list[Row]) -> Optional[tuple]:
    """Mean checker calls of two solvers on the problems BOTH solved: (n, mean first, mean second).

    Comparing each solver's mean over its own solved set is misleading (the
    solver that cracks harder problems looks more expensive)."""
    other = {r.id: r for r in second if r.solved}
    pairs = [(r.checker_calls, other[r.id].checker_calls) for r in first if r.solved and r.id in other]
    if not pairs:
        return None
    return len(pairs), round(sum(a for a, _ in pairs) / len(pairs), 1), round(sum(b for _, b in pairs) / len(pairs), 1)


def full_eval(checkpoint, tag: str, heldout: int = 200, baseline_budgets=(SEARCH_BUDGET, 2000),
              device: str = "auto", workers: int = 8, big_budget: int = 0, value_weight: float = 0.0,
              diverse: bool = True, seeds: int = 1) -> tuple[dict, dict]:
    """The three-mode evaluation on every benchmark.

    Returns (results, spreads): ``results[suite][solver label]`` is the list of
    rows from the first sampling seed, and ``spreads[suite][label]`` the
    number solved for each sampling seed (network rows only; the other
    solvers are run once). Everything is also saved under results/.

    ``big_budget`` > 0 adds a network search with that many checker calls on
    the seed and real suites (to compare with brute force at the same budget).
    ``value_weight`` > 0 makes the network searches rank states with the value head too.
    ``diverse`` samples each state's proposals at a spread of temperatures
    (``model.DIVERSE``); False uses temperature 1 for every sample (the first
    evaluation, M5, used 0.7 without backtracking and 1.0 in search).
    ``seeds`` repeats every trained-network row with that many sampling seeds:
    one sampling run is noisy, and the range says how noisy.
    """
    import random

    import torch

    from .bench import load_real, load_seed
    from .model import DIVERSE, ModelConfig, NeuralProposer, PolicyValueNet, load_model, pick_device
    from .search import UniformProposer

    dev = pick_device(device)
    temperature = DIVERSE if diverse else 1.0
    model = None
    if checkpoint is not None and pathlib.Path(checkpoint).exists():
        model, _ = load_model(checkpoint, dev)
    else:
        print(f"No checkpoint at {checkpoint}: the trained-network rows are skipped. "
              "(Train one with 'alphafe train' and copy it to checkpoints/best.pt.)")
    torch.manual_seed(0)
    untrained = PolicyValueNet(model.config if model is not None else ModelConfig()).to(dev)
    suites = {"seed": load_seed()}
    real = load_real()
    if real:
        suites["real"] = real
    for tier, benches in synthetic_heldout(heldout).items():
        suites[f"synthetic-tier{tier}"] = benches

    out: dict = {}
    spreads: dict = {}
    for suite, benches in suites.items():
        runs: dict = {}
        spread: dict = {}

        def network_rows(label, mode, budget, weight):
            for index in range(seeds):
                torch.manual_seed(1000 + index)
                rows = run_policy(benches, NeuralProposer(model, dev, temperature=temperature), mode, budget,
                                  value_weight=weight)
                spread.setdefault(label, []).append(sum(r.solved for r in rows))
                if index == 0:
                    runs[label] = rows

        if model is not None:
            network_rows(f"network, no backtracking ({GREEDY_BUDGET} calls)", "greedy", GREEDY_BUDGET, 0.0)
            network_rows(f"network, search ({SEARCH_BUDGET} calls)", "search", SEARCH_BUDGET, value_weight)
            if big_budget and suite in ("seed", "real"):
                network_rows(f"network, search ({big_budget} calls)", "search", big_budget, value_weight)
        torch.manual_seed(1000)
        references = (
            ("untrained network", lambda: NeuralProposer(untrained, dev, temperature=temperature)),
            ("uniform policy", lambda: UniformProposer(random.Random(0))),
        )
        for name, make in references:
            runs[f"{name}, no backtracking ({GREEDY_BUDGET} calls)"] = run_policy(benches, make(), "greedy", GREEDY_BUDGET)
            runs[f"{name}, search ({SEARCH_BUDGET} calls)"] = run_policy(benches, make(), "search", SEARCH_BUDGET)
        budgets = list(baseline_budgets) + ([big_budget] if big_budget and big_budget not in baseline_budgets else [])
        for budget in budgets:
            runs[f"brute force ({budget} calls)"] = run_baseline(benches, budget, 120.0, workers=workers)
        for label, rows in runs.items():
            slug = label.replace(",", "").replace("(", "").replace(")", "").replace(" ", "_")
            save(f"{tag}_{suite}_{slug}", rows, {"suite": suite, "solver": label, "checkpoint": str(checkpoint),
                                                 "solved_per_seed": spread.get(label)})
        out[suite] = runs
        spreads[suite] = spread
        if dev.type == "mps":
            torch.mps.empty_cache()
    return out, spreads


def report(results: dict, spreads: Optional[dict] = None) -> str:
    """Markdown tables for a ``full_eval`` result."""
    parts = []
    for suite, runs in results.items():
        n = len(next(iter(runs.values())))
        parts.append(f"#### {suite} ({n} problems)\n")
        parts.append(markdown_summary(runs))
        spread = (spreads or {}).get(suite, {})
        multi = {label: counts for label, counts in spread.items() if len(counts) > 1}
        if multi:
            parts.append("")
            parts.append("Solved per sampling seed: " + "; ".join(f"{label}: {counts}" for label, counts in multi.items()))
        pairs = []
        for label, rows in runs.items():
            if not label.startswith("network"):
                continue
            budget = label[label.index("(") + 1: label.index(" calls")]
            rival = runs.get(f"brute force ({budget} calls)") or runs.get(f"brute force ({SEARCH_BUDGET} calls)")
            both = common_calls(rows, rival) if rival else None
            if both:
                pairs.append(f"{label}: {both[1]} calls vs brute force {both[2]} on the {both[0]} problems both solve")
        if pairs:
            parts.append("")
            parts.append("Mean checker calls on commonly solved problems: " + "; ".join(pairs) + ".")
        if suite in ("seed", "real"):
            parts.append("")
            parts.append(markdown_by_mohs(runs))
        parts.append("")
    return "\n".join(parts)


def main(argv=None) -> None:
    import argparse

    parser = argparse.ArgumentParser(
        prog="alphafe eval",
        description="Three-mode evaluation on all benchmarks (seed, real, held-out synthetic). "
                    "Without a checkpoint the trained-network rows are skipped and the references still run.")
    parser.add_argument("--checkpoint", default=str(ROOT / "checkpoints" / "best.pt"))
    parser.add_argument("--tag", default="eval", help="prefix for the files written to results/")
    parser.add_argument("--heldout", type=int, default=200, help="held-out synthetic problems per tier")
    parser.add_argument("--device", default="auto")
    parser.add_argument("--big-budget", type=int, default=0,
                        help="also run the network search with this many checker calls on seed/real")
    parser.add_argument("--value-weight", type=float, default=0.0,
                        help="rank search states by policy log-probability plus this times log(value)")
    parser.add_argument("--single-temperature", action="store_true",
                        help="sample all proposals at temperature 1 instead of a spread")
    parser.add_argument("--seeds", type=int, default=1, help="sampling seeds for the trained-network rows")
    args = parser.parse_args(argv)
    results, spreads = full_eval(args.checkpoint, args.tag, heldout=args.heldout, device=args.device,
                                 big_budget=args.big_budget, value_weight=args.value_weight,
                                 diverse=not args.single_temperature, seeds=args.seeds)
    text = report(results, spreads)
    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / f"{args.tag}.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
