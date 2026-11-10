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
