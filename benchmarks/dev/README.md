# Development suite

Problems harder than the seed set, mostly rated 10M and above, that may be
looked at, diagnosed and tuned on. `alphafe eval --suite dev` runs them. The
real benchmark answers "how good is it"; this suite answers "what should be
worked on next".

The suite has 32 problems:

* `dev.jsonl` (20 problems). Ten come from the design study behind issue
  #99, which probed well-known problems by hand before the real benchmark
  existed. Ten more were added afterwards from memory.
* The 12 problems of `benchmarks/real/real.jsonl` flagged
  `"seen_in_development": true`. They are loaded from that file and not
  copied here.

USAMO 2002/4, the other study problem, is seed problem `s51`.

## How the problems were chosen

They were hand-picked, with knowledge of what the solver can and cannot do,
so results on this suite say nothing about how good the solver is.

A candidate was dropped, without running the solver on it, when it was the
same equation as an unflagged real problem or a seed problem up to renaming
variables, replacing a variable by its negative, or replacing f by -f. Seven
candidates went that way for the real set and seven for the seed set.
`tests/test_dev.py` repeats the check on every run.

Each answer was checked by `scripts/validate_bench.py`: every listed function
satisfies the equation, and no polynomial of degree at most 2 is missing.
That the answer is complete beyond that rests on the problem being well
known. The MOHS numbers are rough estimates.

## Proofs

`proofs/<id>.proof` are hand-written proofs that the checker accepts, 13 so
far. They exist for diagnosis (`scripts/diagnose.py --suite dev` shows where
a search loses the thread) and are never used as training data. Dev problems
and their twins are also kept out of the synthetic training pool.
