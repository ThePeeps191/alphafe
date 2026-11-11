"""Evaluation: run solvers over benchmarks and tabulate solve rate, checker calls and time."""

from __future__ import annotations

import datetime
import hashlib
import json
import multiprocessing as mp
import pathlib
import platform
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from typing import Optional

from .bench import ROOT, AnswerMismatch, BenchProblem, canary
from .env import SearchResult
from .moves import show_proof

RESULTS_DIR = ROOT / "results"
# Record fields that mark a benchmark problem as not fully unseen (benchmarks/real/README.md).
FLAGS = ("in_training_pool", "seen_in_development")


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
    solutions: list = field(default_factory=list)   # the answer as strings that parse_solution_set reads back
    flags: list = field(default_factory=list)       # which of FLAGS the benchmark record carries


MISMATCH_REASON = "answer mismatch: not scored"


def score(bench: BenchProblem, result: SearchResult, mismatches: Optional[list] = None, solver: str = "") -> Row:
    """Turn a search result into a table row.

    A checked proof whose answer differs from the recorded one is never
    scored as solved. Without ``mismatches`` it raises ``AnswerMismatch``.
    With a list, the mismatch (problem, both answers, solver and the accepted
    proof) is appended to it and the row is marked unsolved, so that the rest
    of an evaluation survives; the caller must then report the list and fail.
    """
    solved, reason = result.solved, result.reason
    proof = show_proof(result.proof) if result.solved else ""
    if solved:
        try:
            canary(bench, result.solutions, proof=proof, solver=solver)
        except AnswerMismatch as err:
            if mismatches is None:
                raise
            mismatches.append({
                "id": bench.id, "equation": bench.problem.equation, "domain": bench.problem.domain,
                "recorded": [str(f) for f in bench.expected.families], "found": [str(f) for f in result.solutions.families],
                "found_text": str(result.solutions), "solver": solver, "checker_calls": result.checker_calls,
                "proof": proof, "message": str(err),
            })
            solved, reason = False, MISMATCH_REASON
    return Row(
        id=bench.id, equation=bench.problem.equation, domain=bench.problem.domain, mohs=bench.mohs,
        solved=solved, checker_calls=result.checker_calls, seconds=round(result.seconds, 3),
        proof_len=len(result.proof), answer=str(result.solutions) if solved else "",
        reason=reason, proof=proof if solved else "",
        solutions=[str(f) for f in result.solutions.families] if solved else [],
        flags=[name for name in FLAGS if bench.meta.get(name)],
    )


def _baseline_job(args) -> SearchResult:
    from .baseline.search import brute_force

    problem, max_calls, max_seconds, widening = args
    return brute_force(problem, max_calls=max_calls, max_seconds=max_seconds, widening=widening)


def run_baseline(benches: list[BenchProblem], max_calls: int, max_seconds: float, workers: int = 8,
                 widening: bool = True, mismatches: Optional[list] = None, solver: str = "brute force") -> list[Row]:
    """Brute-force baseline over a list of problems, in parallel."""
    jobs = [(b.problem, max_calls, max_seconds, widening) for b in benches]
    if workers <= 1:
        results = [_baseline_job(j) for j in jobs]
    else:
        with mp.get_context("spawn").Pool(workers) as pool:
            results = pool.map(_baseline_job, jobs)
    return [score(b, r, mismatches, solver) for b, r in zip(benches, results)]


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


def unflagged(rows: list[Row]) -> list[Row]:
    """The rows whose benchmark record carries none of ``FLAGS``."""
    return [r for r in rows if not r.flags]


def _git(*args) -> str:
    try:
        done = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return ""
    return done.stdout.strip() if done.returncode == 0 else ""


def tree_is_dirty() -> bool:
    """Are there uncommitted changes to tracked files? (False outside a git checkout.)"""
    return bool(_git("status", "--porcelain", "--untracked-files=no"))


def _portable_path(path) -> str:
    """A path as it is written into result files: relative to the repository, or the bare file name.

    Result files are committed, so they must not carry a home directory.
    """
    path = pathlib.Path(path).resolve()
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.name


def provenance(checkpoint=None, device=None, settings: Optional[dict] = None) -> dict:
    """What produced a result file: code version, weights, machine and settings."""
    commit = _git("rev-parse", "HEAD")
    out = {
        "commit": commit or None,
        "dirty": tree_is_dirty() if commit else None,
        "time_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "torch": getattr(sys.modules.get("torch"), "__version__", None),
        "device": str(device) if device is not None else None,
    }
    if checkpoint is not None and pathlib.Path(checkpoint).exists():
        out["checkpoint"] = _portable_path(checkpoint)
        out["checkpoint_sha256"] = hashlib.sha256(pathlib.Path(checkpoint).read_bytes()).hexdigest()
    else:
        out["checkpoint"] = out["checkpoint_sha256"] = None
    out["settings"] = dict(settings or {})
    return out


def save(name: str, rows: list[Row], config: dict, provenance_block: Optional[dict] = None,
         per_seed: Optional[list] = None) -> pathlib.Path:
    """Write a run to results/<name>.json (small, committed; the source for RESULTS.md tables).

    ``rows`` are the rows of the first sampling seed. ``per_seed`` holds every
    sampling seed's rows; they are stored compactly as {problem id: [solved,
    checker calls]} so that paired comparisons can use all seeds.
    """
    RESULTS_DIR.mkdir(exist_ok=True)
    path = RESULTS_DIR / f"{name}.json"
    payload = {"name": name, "config": config,
               "provenance": provenance_block if provenance_block is not None else provenance(),
               "summary": summary(rows), "by_mohs": by_mohs(rows)}
    if any(r.flags for r in rows):
        payload["summary_unflagged"] = summary(unflagged(rows))
        payload["by_mohs_unflagged"] = by_mohs(unflagged(rows))
    if per_seed is not None:
        payload["per_seed"] = [{r.id: [int(r.solved), r.checker_calls] for r in seed_rows} for seed_rows in per_seed]
    payload["rows"] = [asdict(r) for r in rows]
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
               value_weight: float = 0.0, mismatches: Optional[list] = None, solver: str = "") -> list[Row]:
    """Run a proposer (network or uniform) over problems. mode: 'greedy' or 'search'."""
    from .search import BestFirstSearch, GreedySearch, run_searches

    # The network reads only the variables x, y, z; a problem written in other letters is renamed for the search.
    problems = [b.problem.standard_names()[0] for b in benches]
    if mode == "greedy":
        searches = [GreedySearch(p, budget=budget) for p in problems]
    else:
        searches = [BestFirstSearch(p, budget=budget, value_weight=value_weight) for p in problems]
    began = time.time()
    run_searches(searches, proposer, k)
    elapsed = (time.time() - began) / max(1, len(benches))
    rows = []
    for bench, search in zip(benches, searches):
        result = search.result()
        result.seconds = elapsed      # searches run interleaved; report the average share
        rows.append(score(bench, result, mismatches, solver or mode))
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


SUITE_CHOICES = ("seed", "real", "synthetic", "synthetic-tier1", "synthetic-tier2", "synthetic-tier3", "synthetic-tier4")
BIG_BUDGET_SUITES = ("seed", "real")      # the suites that get the --big-budget rows (network and brute force)
SAMPLING_SEED = 1000                      # sampling seed i of a network row is SAMPLING_SEED + i


@dataclass
class EvalRun:
    """Everything a ``full_eval`` call produced. Unpacks as ``results, spreads`` for older callers."""

    results: dict          # results[suite][solver label] = rows of the first sampling seed
    spreads: dict          # spreads[suite][label] = number solved per sampling seed (network rows only)
    seed_rows: dict        # seed_rows[suite][label] = the rows of every sampling seed
    mismatches: list       # answer mismatches found (each also written to results/<tag>_MISMATCH_<id>.json)
    provenance: dict

    def __iter__(self):
        return iter((self.results, self.spreads))


def select_suites(names, heldout: int = 200) -> dict:
    """The benchmark suites to evaluate, in the usual order. ``names`` None or empty means all."""
    from .bench import load_real, load_seed

    wanted = set(names or ())
    unknown = wanted - set(SUITE_CHOICES)
    if unknown:
        raise ValueError(f"unknown suite: {', '.join(sorted(unknown))} (choose from {', '.join(SUITE_CHOICES)})")

    def want(name: str) -> bool:
        return not wanted or name in wanted or (name.startswith("synthetic") and "synthetic" in wanted)

    suites: dict = {}
    if want("seed"):
        suites["seed"] = load_seed()
    if want("real"):
        real = load_real()
        if real:
            suites["real"] = real
    if not wanted or any(name.startswith("synthetic") for name in wanted):
        for tier, benches in synthetic_heldout(heldout).items():
            if want(f"synthetic-tier{tier}"):
                suites[f"synthetic-tier{tier}"] = benches
    return suites


def full_eval(checkpoint, tag: Optional[str] = "eval", heldout: int = 200, baseline_budgets=(SEARCH_BUDGET, 2000),
              device: str = "auto", workers: int = 8, big_budget: int = 0, value_weight: float = 0.0,
              diverse: bool = True, seeds: int = 1, suites=None, mismatches: Optional[list] = None,
              baseline_seconds: float = 120.0) -> EvalRun:
    """The three-mode evaluation on the chosen benchmarks (all of them by default).

    Returns an ``EvalRun``; ``results, spreads = full_eval(...)`` also works.
    ``results[suite][solver label]`` is the list of rows from the first
    sampling seed, and ``spreads[suite][label]`` the number solved for each
    sampling seed (network rows only; the other solvers are run once).
    Everything is also saved under results/, named ``<tag>_<suite>_<solver>``
    (or ``<suite>_<solver>`` when ``tag`` is None).

    ``suites`` restricts the run: any of ``SUITE_CHOICES``.
    ``big_budget`` > 0 adds a network search and a brute-force run with that
    many checker calls on the seed and real suites.
    ``value_weight`` > 0 makes the network searches rank states with the value head too.
    ``diverse`` samples each state's proposals at a spread of temperatures
    (``model.DIVERSE``); False uses temperature 1 for every sample (the first
    evaluation, M5, used 0.7 without backtracking and 1.0 in search).
    ``seeds`` repeats every trained-network row with that many sampling seeds:
    one sampling run is noisy, and the range says how noisy.
    ``mismatches``: see ``score``. If the caller passes no list, the run is
    still finished and saved, and ``AnswerMismatch`` is raised at the end.

    A problem's row depends on which other problems share its suite, because
    all searches of a suite draw from one random stream. Rows are comparable
    between runs only for an identical suite.
    """
    import random

    import torch

    from .model import DIVERSE, ModelConfig, NeuralProposer, PolicyValueNet, load_model, pick_device
    from .search import UniformProposer

    if big_budget in (GREEDY_BUDGET, SEARCH_BUDGET):
        raise ValueError(f"--big-budget {big_budget} is the budget of a standard row; its results would overwrite that row")
    raise_at_end = mismatches is None
    found: list = [] if mismatches is None else mismatches
    dev = pick_device(device)
    temperature = DIVERSE if diverse else 1.0
    model = None
    if checkpoint is not None and pathlib.Path(checkpoint).exists():
        model, _ = load_model(checkpoint, dev)
    else:
        print(f"No checkpoint at {checkpoint}: the trained-network rows are skipped. "
              "(Train one with 'alphafe train' and copy it to checkpoints/best.pt, or download one: see README.)")
    torch.manual_seed(0)
    untrained = PolicyValueNet(model.config if model is not None else ModelConfig()).to(dev)
    chosen = select_suites(suites, heldout)
    stamp = provenance(checkpoint if model is not None else None, dev, {
        "suites": list(chosen), "heldout_per_tier": heldout, "sampling_seeds": [SAMPLING_SEED + i for i in range(seeds)],
        "proposals_per_state": PROPOSALS, "temperature": list(temperature) if isinstance(temperature, (list, tuple)) else temperature,
        "value_weight": value_weight, "greedy_budget": GREEDY_BUDGET, "search_budget": SEARCH_BUDGET,
        "big_budget": big_budget, "baseline_budgets": list(baseline_budgets), "baseline_seconds": baseline_seconds,
        "baseline_workers": workers,
    })

    out: dict = {}
    spreads: dict = {}
    every_seed: dict = {}
    for suite, benches in chosen.items():
        runs: dict = {}
        spread: dict = {}
        per_seed: dict = {}

        def network_rows(label, mode, budget, weight):
            for index in range(seeds):
                torch.manual_seed(SAMPLING_SEED + index)
                rows = run_policy(benches, NeuralProposer(model, dev, temperature=temperature), mode, budget,
                                  value_weight=weight, mismatches=found, solver=f"{label}, sampling seed {SAMPLING_SEED + index}")
                spread.setdefault(label, []).append(sum(r.solved for r in rows))
                per_seed.setdefault(label, []).append(rows)
                if index == 0:
                    runs[label] = rows

        if model is not None:
            network_rows(f"network, no backtracking ({GREEDY_BUDGET} calls)", "greedy", GREEDY_BUDGET, 0.0)
            network_rows(f"network, search ({SEARCH_BUDGET} calls)", "search", SEARCH_BUDGET, value_weight)
            if big_budget and suite in BIG_BUDGET_SUITES:
                network_rows(f"network, search ({big_budget} calls)", "search", big_budget, value_weight)
        torch.manual_seed(SAMPLING_SEED)
        references = (
            ("untrained network", lambda: NeuralProposer(untrained, dev, temperature=temperature)),
            ("uniform policy", lambda: UniformProposer(random.Random(0))),
        )
        for name, make in references:
            for mode, word, budget in (("greedy", "no backtracking", GREEDY_BUDGET), ("search", "search", SEARCH_BUDGET)):
                label = f"{name}, {word} ({budget} calls)"
                runs[label] = run_policy(benches, make(), mode, budget, mismatches=found, solver=label)
        budgets = list(baseline_budgets)
        if big_budget and big_budget not in budgets and suite in BIG_BUDGET_SUITES:
            budgets.append(big_budget)
        for budget in budgets:
            label = f"brute force ({budget} calls)"
            runs[label] = run_baseline(benches, budget, baseline_seconds, workers=workers, mismatches=found, solver=label)
        for label, rows in runs.items():
            slug = label.replace(",", "").replace("(", "").replace(")", "").replace(" ", "_")
            name = f"{tag}_{suite}_{slug}" if tag else f"{suite}_{slug}"
            save(name, rows, {"suite": suite, "solver": label,
                              "checkpoint": stamp["checkpoint"] if label.startswith("network") else None,
                              "solved_per_seed": spread.get(label)},
                 provenance_block=stamp, per_seed=per_seed.get(label))
        out[suite] = runs
        spreads[suite] = spread
        every_seed[suite] = {label: per_seed.get(label, [rows]) for label, rows in runs.items()}
        if dev.type == "mps":
            torch.mps.empty_cache()
    for index, item in enumerate(found):
        RESULTS_DIR.mkdir(exist_ok=True)
        (RESULTS_DIR / f"{tag or 'eval'}_MISMATCH_{item['id']}_{index}.json").write_text(json.dumps(item, indent=1) + "\n")
    run = EvalRun(out, spreads, every_seed, found, stamp)
    if found and raise_at_end:
        raise AnswerMismatch(mismatch_text(found))
    return run


def mismatch_text(mismatches: list) -> str:
    lines = [f"{len(mismatches)} checked proof(s) gave an answer different from the recorded one. Either the record "
             "is wrong or the checker is unsound; no such row was scored as solved."]
    for item in mismatches:
        lines.append(item["message"])
    return "\n\n".join(lines)


def _flag_counts(rows: list[Row]) -> str:
    parts = []
    for name, words in (("seen_in_development", "seen in development"), ("in_training_pool", "in the training pool")):
        count = sum(name in r.flags for r in rows)
        if count:
            parts.append(f"{count} {words}")
    return ", ".join(parts)


def report(results: dict, spreads: Optional[dict] = None, seed_rows: Optional[dict] = None) -> str:
    """Markdown tables for a ``full_eval`` result.

    For a suite with flagged problems (``FLAGS``) every table is given twice:
    on all problems, and on the problems that carry no flag. ``seed_rows``
    (``EvalRun.seed_rows``) lets the second one show the per-seed counts too.
    """
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
        first = next(iter(runs.values()))
        flagged = [r for r in first if r.flags]
        if flagged:
            clean = {label: unflagged(rows) for label, rows in runs.items()}
            parts.append("")
            parts.append(f"Without the {len(flagged)} flagged problems ({_flag_counts(first)}): {n - len(flagged)} problems\n")
            parts.append(markdown_summary(clean))
            per_seed = (seed_rows or {}).get(suite, {})
            multi = {label: [sum(r.solved for r in unflagged(rows)) for rows in lists]
                     for label, lists in per_seed.items() if len(lists) > 1}
            if multi:
                parts.append("")
                parts.append("Solved per sampling seed: " + "; ".join(f"{label}: {counts}" for label, counts in multi.items()))
            parts.append("")
            parts.append(markdown_by_mohs(clean))
        parts.append("")
    return "\n".join(parts)


def main(argv=None) -> None:
    import argparse

    default_checkpoint = ROOT / "checkpoints" / "best.pt"
    parser = argparse.ArgumentParser(
        prog="alphafe eval",
        description="Three-mode evaluation on the benchmarks (seed, real, held-out synthetic). "
                    "Without a checkpoint the trained-network rows are skipped and the references still run.")
    parser.add_argument("--checkpoint", default=None,
                        help="weights to evaluate (default: checkpoints/best.pt if it exists; a path given here must exist)")
    parser.add_argument("--suite", action="append", choices=SUITE_CHOICES, metavar="NAME",
                        help=f"evaluate only this suite; repeatable (default: all). One of: {', '.join(SUITE_CHOICES)}")
    parser.add_argument("--tag", default=None,
                        help="prefix for the files written to results/ (default: 'eval', or none when one --suite is given)")
    parser.add_argument("--heldout", type=int, default=200, help="held-out synthetic problems per tier")
    parser.add_argument("--device", default="auto")
    parser.add_argument("--big-budget", type=int, default=0,
                        help="also run the network search and brute force with this many checker calls on seed/real")
    parser.add_argument("--value-weight", type=float, default=0.0,
                        help="rank search states by policy log-probability plus this times log(value)")
    parser.add_argument("--single-temperature", action="store_true",
                        help="sample all proposals at temperature 1 instead of a spread")
    parser.add_argument("--seeds", type=int, default=1, help="sampling seeds for the trained-network rows")
    parser.add_argument("--workers", type=int, default=8, help="processes for the brute-force rows")
    parser.add_argument("--allow-dirty", action="store_true",
                        help="run although tracked files have uncommitted changes (the result files record that)")
    args = parser.parse_args(argv)
    if args.checkpoint is not None and not pathlib.Path(args.checkpoint).exists():
        parser.error(f"no checkpoint at {args.checkpoint}")
    if args.big_budget in (GREEDY_BUDGET, SEARCH_BUDGET):
        parser.error(f"--big-budget {args.big_budget} is the budget of a standard row; choose another number")
    if tree_is_dirty() and not args.allow_dirty:
        parser.error("tracked files have uncommitted changes, so the results could not be tied to a commit; "
                     "commit first, or pass --allow-dirty")
    one_suite = args.suite is not None and len(set(args.suite)) == 1 and args.suite[0] != "synthetic"
    tag = args.tag if args.tag is not None else (None if one_suite else "eval")
    mismatches: list = []
    run = full_eval(args.checkpoint if args.checkpoint is not None else default_checkpoint, tag,
                    heldout=args.heldout, device=args.device, big_budget=args.big_budget, value_weight=args.value_weight,
                    diverse=not args.single_temperature, seeds=args.seeds, suites=args.suite, mismatches=mismatches,
                    workers=args.workers)
    text = report(run.results, run.spreads, run.seed_rows)
    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / f"{tag or args.suite[0]}.md").write_text(text)
    print(text)
    if mismatches:
        print(mismatch_text(mismatches), file=sys.stderr)
        print(f"\nThe accepted proofs are in results/{tag or 'eval'}_MISMATCH_*.json.", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
