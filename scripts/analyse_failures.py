"""Sort a solver's failures on the seed benchmark into three groups.

    python scripts/analyse_failures.py results/<file>.json [more.json ...]

* "language cannot express the proof": no proof in the move language is known
  (there is no hand-written proof in benchmarks/seed/proofs and no solver has
  ever produced one);
* "the proof is too deep": a proof is known, and the shortest known one needs
  at least DEEP creative moves (moves other than the free ones);
* "the network did not find it": a short proof is known.
"""
import json
import pathlib
import sys

from alphafe.bench import BENCH_DIR, load_seed
from alphafe.env import FREE_MOVES
from alphafe.moves import parse_proof

DEEP = 5


def creative(proof) -> int:
    return sum(1 for move in proof if move not in FREE_MOVES)


def known_proof_lengths() -> dict:
    """Shortest known number of creative moves per seed problem, from hand proofs and saved results."""
    best: dict = {}
    for path in (BENCH_DIR / "seed" / "proofs").glob("*.proof"):
        best[path.stem] = creative(parse_proof(path.read_text()))
    for path in pathlib.Path("results").glob("*.json"):
        for row in json.loads(path.read_text())["rows"]:
            if row["solved"] and row["id"].startswith("s") and row["proof"]:
                n = creative(parse_proof(row["proof"]))
                best[row["id"]] = min(best.get(row["id"], n), n)
    return best


def main() -> None:
    lengths = known_proof_lengths()
    seeds = {b.id: b for b in load_seed()}
    for name in sys.argv[1:]:
        payload = json.loads(pathlib.Path(name).read_text())
        groups = {"language cannot express the proof": [], "the proof is too deep": [], "the network did not find it": []}
        for row in payload["rows"]:
            if row["solved"] or row["id"] not in seeds:
                continue
            n = lengths.get(row["id"])
            if n is None:
                groups["language cannot express the proof"].append(row["id"])
            elif n >= DEEP:
                groups["the proof is too deep"].append(f"{row['id']} ({n} moves)")
            else:
                groups["the network did not find it"].append(f"{row['id']} ({n} moves)")
        solved = sum(r["solved"] for r in payload["rows"])
        print(f"{payload['config'].get('solver', name)}: solved {solved}/{len(payload['rows'])}")
        for group, ids in groups.items():
            print(f"  {group}: {len(ids)}  {', '.join(ids)}")


if __name__ == "__main__":
    main()
