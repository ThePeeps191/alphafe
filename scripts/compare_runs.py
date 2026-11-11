"""Side-by-side table of evaluations: python scripts/compare_runs.py TAG [TAG ...]

For every suite and solver, prints the number solved for each tag; for
trained-network rows evaluated with several sampling seeds it prints the
range. Brute-force and reference rows are taken from the first tag.
"""
import json
import sys

from alphafe.bench import ROOT

SUITES = ["seed", "real", "synthetic-tier1", "synthetic-tier2", "synthetic-tier3", "synthetic-tier4"]


def load(tag: str) -> dict:
    out: dict = {}
    for path in sorted((ROOT / "results").glob(f"{tag}_*.json")):
        payload = json.loads(path.read_text())
        config = payload.get("config", {})
        if "suite" in config:
            out[(config["suite"], config["solver"])] = payload
    return out


def cell(payload) -> str:
    if payload is None:
        return "-"
    counts = payload["config"].get("solved_per_seed")
    n = payload["summary"]["problems"]
    if counts and len(counts) > 1:
        return f"{min(counts)}-{max(counts)}" if min(counts) != max(counts) else f"{counts[0]}"
    return f"{payload['summary']['solved']}"


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        sys.exit(__doc__)
    tags = sys.argv[1:]
    data = {tag: load(tag) for tag in tags}
    for suite in SUITES:
        solvers = [solver for (s, solver) in data[tags[0]] if s == suite]
        if not solvers:
            continue
        n = next(p["summary"]["problems"] for (s, _), p in data[tags[0]].items() if s == suite)
        print(f"\n{suite} ({n} problems): number solved")
        network = sorted(s for s in solvers if s.startswith("network"))
        others = sorted(s for s in solvers if not s.startswith("network"))
        print("| solver | " + " | ".join(tags) + " |")
        print("|---|" + "---|" * len(tags))
        for solver in network:
            print(f"| {solver} | " + " | ".join(cell(data[t].get((suite, solver))) for t in tags) + " |")
        for solver in others:
            print(f"| {solver} | " + " | ".join(cell(data[t].get((suite, solver))) for t in tags) + " |")


if __name__ == "__main__":
    main()
