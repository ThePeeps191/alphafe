"""Write held-out problems with known proofs of several moves to benchmarks/synthetic/planted.jsonl.

    .venv/bin/python scripts/freeze_planted.py --check     # regenerate in memory and compare with the file
    .venv/bin/python scripts/freeze_planted.py --force     # overwrite the file

A problem here is a generated problem hidden behind one to three changes of
variables (``generate.disguise``). Its proof is known by construction
(``planted.planted_proof``): undo the changes, then make the opening
substitutions into the plain equation. The file sorts the problems by the
number of proposed moves in that proof (2, 3 or 4), which the evaluation
reads as the suites ``planted-2``, ``planted-3`` and ``planted-4``.

The known proof is an upper bound: a search may find a shorter one. The
suites therefore measure what a solver does on problems that are known to
have a proof of that length, and brute force on the same problems says how
hard they are in practice.

Five of the sixteen changes of variables are never used by a training pool
(``generate.HELD_OUT_CHANGES``). A line with ``unseen_change`` true needs an
undo move of a shape the trainer was never shown, so results are also
reported for those lines alone.

Nothing here can reach a training pool. Every plain problem behind a line of
the file has split == "test" by its canonical hash, so a pool neither
contains it nor disguises it, and ``generate.protected_keys`` excludes the
hidden equations, the plain ones and their twins.
"""
import argparse
import json
import multiprocessing
import sys

from alphafe.bench import BENCH_DIR
from alphafe.checker import Reject
from alphafe.env import start
from alphafe.generate import HELD_OUT_CHANGES, disguise, protected_keys
from alphafe.moves import show_move
from alphafe.planted import planted_proof
from alphafe.train import ProblemPool

import random

PER_LENGTH = 200
LENGTHS = (2, 3, 4)
ATTEMPTS = 4           # disguises tried per plain problem and number of layers
FILE = "planted.jsonl"


def one(job):
    """One disguise of one plain problem: a record with its known proof, or None."""
    base, layers, attempt = job
    hidden = disguise(base, random.Random(f"planted:{base.key}:{layers}:{attempt}"), layers)
    if hidden is None:
        return None
    try:
        if start(hidden.problem())[0].solved:
            return None
    except Reject:
        return None
    proof = planted_proof(hidden)
    if proof is None or len(proof) not in LENGTHS:
        return None
    return {"id": hidden.key[:10], "equation": hidden.equation, "domain": hidden.domain, "tier": base.tier,
            "moves": len(proof), "layers": layers, "plain": hidden.plain, "proof": [show_move(move) for move in proof],
            "key": hidden.key, "base": base.key, "attempt": attempt, "source": f"planted-{len(proof)}",
            "changes": list(hidden.changes), "unseen_change": any(index in HELD_OUT_CHANGES for index in hidden.changes)}


def lines(processes: int) -> list:
    pool = ProblemPool(seed=0, per_tier=3000)            # the pool the held-out tiers were cut from
    bases = [item for items in pool.test.values() for item in items]
    assert all(base.split == "test" for base in bases)
    # One attempt for every problem before the next attempt for any: the file then draws on as many plain
    # problems as possible.
    jobs = [(base, layers, attempt) for attempt in range(ATTEMPTS) for layers in (1, 2, 3) for base in bases]
    with multiprocessing.get_context("spawn").Pool(processes) as helpers:
        records = helpers.map(one, jobs, chunksize=16)
    taken = {base.key for base in bases} | {json.loads(line)["key"] for line in
                                           (BENCH_DIR / "synthetic" / "heldout.jsonl").read_text().splitlines() if line.strip()}
    chosen = {length: [] for length in LENGTHS}
    for record in records:
        if record is None or record["key"] in taken or len(chosen[record["moves"]]) >= PER_LENGTH:
            continue
        taken.add(record["key"])
        del record["attempt"]
        chosen[record["moves"]].append(json.dumps(record))
    return [line for length in LENGTHS for line in chosen[length]]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Regenerate the frozen set of problems with known proofs (compare by default).")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="compare a fresh generation with the file (the default)")
    group.add_argument("--force", action="store_true", help=f"overwrite benchmarks/synthetic/{FILE}")
    parser.add_argument("--processes", type=int, default=8)
    args = parser.parse_args()
    path = BENCH_DIR / "synthetic" / FILE
    fresh = lines(args.processes)
    counts = {length: sum(1 for line in fresh if json.loads(line)["moves"] == length) for length in LENGTHS}
    print("problems by number of proposed moves in the known proof:", counts)
    if args.force:
        path.write_text("\n".join(fresh) + "\n")
        print("wrote", path)
        sys.exit(0)
    current = path.read_text().splitlines() if path.exists() else []
    if current == fresh:
        print(f"{path.name}: a fresh generation gives the same {len(fresh)} problems")
        sys.exit(0)
    same = sum(a == b for a, b in zip(current, fresh))
    print(f"{path.name}: {len(current)} problems in the file, {len(fresh)} generated now, {same} identical line for line")
    print("The file was not changed. Use --force to overwrite it (this redefines the benchmark).")
    sys.exit(1)
