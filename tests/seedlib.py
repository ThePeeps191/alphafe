"""Helpers for loading the seed benchmark in tests."""

import json
import pathlib

from alphafe.checker import Problem
from alphafe.moves import parse_proof
from alphafe.solutions import parse_solution_set

SEED_DIR = pathlib.Path(__file__).resolve().parent.parent / "benchmarks" / "seed"


def load_seeds():
    """Every record of every *.jsonl file in benchmarks/seed."""
    out = []
    for path in sorted(SEED_DIR.glob("*.jsonl")):
        out.extend(json.loads(line) for line in path.read_text().splitlines() if line.strip())
    return out


def seed_problem(record) -> Problem:
    return Problem.parse(record["equation"], record["domain"], record["id"])


def seed_proofs():
    """[(record, proof)] for every hand-written proof."""
    by_id = {r["id"]: r for r in load_seeds()}
    return [(by_id[p.stem], parse_proof(p.read_text())) for p in sorted((SEED_DIR / "proofs").glob("*.proof"))]


def expected(record):
    return parse_solution_set(record["solutions"])
