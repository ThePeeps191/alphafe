"""Loading benchmark problems.

A benchmark file is JSON Lines; each line has ``id``, ``equation``, ``domain``
and optionally ``solutions`` (the full expected answer), ``mohs`` and
``source``. See benchmarks/real/README.md.
"""

from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass, field
from typing import Optional

from .checker import Problem
from .solutions import SolutionSet, parse_solution_set

ROOT = pathlib.Path(__file__).resolve().parent.parent
BENCH_DIR = ROOT / "benchmarks"


@dataclass
class BenchProblem:
    id: str
    problem: Problem
    expected: Optional[SolutionSet]     # None when the answer is not recorded
    mohs: Optional[int] = None
    source: str = ""
    meta: dict = field(default_factory=dict)


def load_file(path) -> list[BenchProblem]:
    out = []
    for line in pathlib.Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        rec = json.loads(line)
        problem = Problem.parse(rec["equation"], rec.get("domain", "R"), rec["id"])
        expected = parse_solution_set(rec["solutions"]) if "solutions" in rec else None
        out.append(BenchProblem(rec["id"], problem, expected, rec.get("mohs"), rec.get("source", ""), rec))
    return out


def load_dir(name: str) -> list[BenchProblem]:
    """All problems in benchmarks/<name>/*.jsonl, in file-name order."""
    out = []
    for path in sorted((BENCH_DIR / name).glob("*.jsonl")):
        out.extend(load_file(path))
    return out


def load_seed() -> list[BenchProblem]:
    return load_dir("seed")


def load_real() -> list[BenchProblem]:
    """Problems added by the project owners (empty until they add some)."""
    return load_dir("real")


class AnswerMismatch(AssertionError):
    """A checked proof produced a solution set different from the recorded answer.

    This must never happen: either the checker is unsound or the recorded
    answer is wrong. It is raised loudly instead of being scored as a failure
    or a success.
    """


def canary(bench: BenchProblem, solutions: SolutionSet) -> None:
    if bench.expected is not None and solutions != bench.expected:
        raise AnswerMismatch(
            f"{bench.id}: {bench.problem.equation}: the checker accepted a proof giving [{solutions}] "
            f"but the recorded answer is [{bench.expected}]"
        )
