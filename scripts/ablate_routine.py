"""Brute force on the seed set and the frozen held-out set with some of the routine moves switched off.

    .venv/bin/python scripts/ablate_routine.py CONFIG CALLS SECONDS OUT.json [WORKERS]

CONFIG is plain (no routine moves: the environment before M8), swapinst
(swap and closed instances), open (plus the opening substitutions at 0 and on
the diagonals), m8 (plus witnesses and the extra preimage targets: the
environment of M8, with its cap of 40 identities per case), ones (plus the
openings at 1 and -1 and a cap of 80) or full (plus the f-term openings: the
default environment).
The output is {suite: {problem id: [solved, checker calls, seconds, stop
reason, proof length]}}. The files behind the M8 table in RESULTS.md are
results/m8_ablation_*.json.
"""
import json, sys, time, pathlib
from alphafe import env
from alphafe.baseline import search as BS
from alphafe.bench import load_seed, BenchProblem
from alphafe.checker import Problem
from alphafe.eval import run_baseline, synthetic_heldout

CONFIGS = {
    "plain":    dict(opening=False, ones=False, fterms=False, swap=False, instances=False, witness=False, pre=["0"], rows=40),
    "swapinst": dict(opening=False, ones=False, fterms=False, swap=True, instances=True, witness=False, pre=["0"], rows=40),
    "open":     dict(opening=True, ones=False, fterms=False, swap=True, instances=True, witness=False, pre=["0"], rows=40),
    "m8":       dict(opening=True, ones=False, fterms=False, swap=True, instances=True, witness=True, pre=["0", "1", "-1", "2"], rows=40),
    "ones":     dict(opening=True, ones=True, fterms=False, swap=True, instances=True, witness=True, pre=["0", "1", "-1", "2"], rows=80),
    "full":     dict(opening=True, ones=True, fterms=True, swap=True, instances=True, witness=True, pre=["0", "1", "-1", "2"], rows=80),
}

def configure(name):
    from alphafe import checker
    cfg = CONFIGS[name]
    for k in env.ROUTINE: env.ROUTINE[k] = cfg[k]
    BS.PRE_POOL[:] = cfg["pre"]
    checker.MAX_ROWS = cfg["rows"]

def job(args):
    name, eq, dom, calls, secs = args
    configure(name)
    from alphafe.baseline.search import brute_force
    r = brute_force(Problem.parse(eq, dom), max_calls=calls, max_seconds=secs)
    return (r.solved, r.checker_calls, round(r.seconds, 3), r.reason, len(r.proof))

if __name__ == "__main__":
    import multiprocessing as mp
    if len(sys.argv) < 5 or sys.argv[1] not in CONFIGS:
        sys.exit(__doc__)
    name, calls, secs, out = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), pathlib.Path(sys.argv[4])
    suites = {"seed": load_seed()}
    for tier, benches in synthetic_heldout(200).items(): suites[f"tier{tier}"] = benches
    result = {}
    t0 = time.time()
    with mp.get_context("spawn").Pool(int(sys.argv[5]) if len(sys.argv) > 5 else 8) as pool:
        for suite, benches in suites.items():
            rows = pool.map(job, [(name, b.problem.equation, b.problem.domain, calls, secs) for b in benches])
            result[suite] = {b.id: row for b, row in zip(benches, rows)}
            solved = sum(r[0] for r in rows); timed = sum(r[3].startswith("time") for r in rows)
            print(f"{name} calls={calls} secs={secs} {suite}: {solved}/{len(rows)} solved, {sum(r[1] for r in rows)} calls, {sum(r[2] for r in rows):.0f}s cpu, time-limited {timed}", flush=True)
    out.write_text(json.dumps(result))
    print(f"wall {time.time()-t0:.0f}s")
