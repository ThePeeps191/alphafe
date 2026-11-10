import random

from alphafe.bench import load_seed
from alphafe.eval import markdown_by_mohs, markdown_summary, report, run_policy, summary
from alphafe.search import UniformProposer


def test_run_policy_scores_with_the_canary_and_formats_tables():
    seeds = load_seed()[:5]
    rows = run_policy(seeds, UniformProposer(random.Random(0)), "search", budget=200)
    assert len(rows) == 5 and all(r.checker_calls <= 200 for r in rows)
    solved = [r for r in rows if r.solved]
    assert len(solved) >= 3 and all(r.proof and r.answer for r in solved)
    greedy = run_policy(seeds, UniformProposer(random.Random(0)), "greedy", budget=32)
    runs = {"search": rows, "greedy": greedy}
    table = markdown_summary(runs)
    assert table.count("\n") == 3 and "| search |" in table
    assert "0M" in markdown_by_mohs(runs)
    text = report({"seed": runs})
    assert "#### seed (5 problems)" in text
    assert summary(rows)["problems"] == 5
