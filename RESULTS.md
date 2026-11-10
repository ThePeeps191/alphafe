# Results

Every number here was produced by the code in this repository. Each run is
saved under `results/` (JSON, one row per problem, with the found proof).
Negative results stay in.

**Definitions.** "Solved" means a complete proof was found *and* re-checked
from scratch by `checker.check`; if a recorded answer exists, the proof's
solution set must equal it (a mismatch aborts the run instead of being
scored). "Checker calls" counts proposed moves sent to the checker, accepted
or not; the free moves applied automatically after each proposal (conclude,
cauchy, inj, surj, cancel) are not counted.

## M3: baselines on the seed benchmark (46 problems)

Hardware: Apple M6, 12 cores, CPU only. Command: `python scripts/run_baseline.py <calls> 120`.

### Brute force

Breadth-first search over a fixed pool of substitution terms (28 single
terms, 15 terms for double substitutions), case splits, preimages, with
duplicate-state merging. "Widening" searches a 5-term pool deeply first, then
a 15-term pool, then the full pool.

| solver | budget (checker calls) | solved | 0M | 5M | 10M | 15M | 20M | mean calls when solved |
|---|---|---|---|---|---|---|---|---|
| brute force, widening | 200 | 26/46 (56.5%) | 20/20 | 5/13 | 1/11 | 0/1 | 0/1 | 8.7 |
| brute force, widening | 2,000 | 33/46 (71.7%) | 20/20 | 10/13 | 3/11 | 0/1 | 0/1 | 154.4 |
| brute force, widening | 20,000 | 37/46 (80.4%) | 20/20 | 12/13 | 5/11 | 0/1 | 0/1 | 1100.0 |
| brute force, plain BFS | 20,000 | 33/46 (71.7%) | 20/20 | 8/13 | 5/11 | 0/1 | 0/1 | 718.4 |
| brute force, plain BFS | 50,000 | 35/46 (76.1%) | 20/20 | 8/13 | 7/11 | 0/1 | 0/1 | 2531.9 |

Unsolved by widening brute force at 20,000 calls: s33, s34 (two nested case
splits), s36, s37, s38, s42, s44, s45, s46.

### Answer guesser

Plugging in `ax^2 + bx + c` and solving for the coefficients gives the
recorded answer on 45/46 seed problems. The miss is s31, whose answer
`x^3 + cx` is not quadratic. The guesser produces answers only, never proofs
that nothing else works.

### Reading

* The checker's automatic normalisation does a lot: every 0M seed problem
  falls to one or two substitutions, so brute force is a strong control at
  the easy end. A network can only beat it on *cost* there (fewer checker
  calls), not on solve rate.
* The room for a learned policy is at 5-10M, where brute force needs
  thousands of calls or fails: proofs needing a specific double substitution,
  a substitution into a derived identity, or two case splits.
* No accepted proof gave an answer different from the recorded one.
