"""Summarise a training log: python scripts/show_log.py <run>"""
import json
import pathlib
import sys

path = pathlib.Path("logs") / sys.argv[1] / "train.jsonl"
for line in path.read_text().splitlines():
    r = json.loads(line)
    extras = {k: v for k, v in r.items() if k.startswith(("heldout", "uniform", "promoted"))}
    if extras or r["iteration"] % 10 == 0:
        print(f"it {r['iteration']:4d} tier {r['tier']} selfplay {r['selfplay_rate_tier']:.2f} calls {r['mean_calls']:5.1f} "
              f"loss {r.get('policy_loss')} iter {r['iter_s']}s min {r['total_minutes']} {extras}")
