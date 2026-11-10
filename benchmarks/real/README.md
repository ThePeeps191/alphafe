# Real benchmark

Real competition problems, used only for testing. Nothing here is used for
training or for choosing between versions of the solver.

* `real.jsonl`: 137 problems, each with its source, the statement as the
  source gives it, the published answer and a MOHS difficulty.
* `SKIPPED.md`: the selection rules, written down before the problems they
  cover were collected, and the other 1,575 problems the rules covered, each
  with the reason it was left out.
* `INSTRUCTIONS.md`: the rules for adding to the benchmark, the file format
  and what `scripts/validate_bench.py` checks.

The problems come from two sources: every problem that
[MathNet](https://mathnet.mit.edu) files under functional equations or that
mentions a function, and every function problem in
[Evan Chen's solution notes](https://web.evanchen.cc/problems.html). A
problem is in the file when it fits the solver's scope exactly as stated.
Whether the solver can do it played no part, with one exception that
`SKIPPED.md` records: USAMO 2002/4 is in scope and was left out because the
solver had already been run on it (issue #2). It will join the seed set, which
is the development set. Two problems with exponents above 2000 are in the
file although the checker refuses to load them; they count as unsolved.

Three of the difficulty numbers are Evan Chen's published ratings
(`"mohs_source": "chen"`). The other 134 are estimates made for this
benchmark, so treat a difficulty band as a rough grouping.

Two flags mark problems that are not fully unseen. Results should be given
with and without them.

* `"in_training_pool": true` (1 problem): the synthetic generator also
  produces this equation, so the published weights may have trained on it.
* `"seen_in_development": true` (12 problems). For 11 of them the solver
  was run on the problem, and proposals for improving it were written with
  the problem in view, before this benchmark existed (the study behind issue
  #99). Version 1 was not changed because of them, so its results on them
  are clean, but later versions cannot claim them as unseen. The twelfth,
  `swiss-mo-2006-1`, is seed problem s31 after a linear change of variables,
  and the seed set was used throughout development.

`alphafe eval` loads every `*.jsonl` file in this directory and reports it as
the `real` suite.
