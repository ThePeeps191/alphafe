# Compiling the real benchmark

Instructions for a coding agent (or a person) asked to fill this directory.
Read all of it before starting. It assumes no other knowledge of the project.

## What this directory is for

AlphaFE is a solver for easy olympiad functional equations (see the README at
the repository root). It is trained only on synthetic problems that a
generator makes up. Two benchmarks exist already: `benchmarks/seed/`, written
for the project and used during development to choose fixes, and
`benchmarks/synthetic/heldout.jsonl`, which comes from the same generator as
the training data. Neither one says how the solver does on problems that
people actually set in competitions.

This directory is that test: real competition problems, with their sources
and known answers, that nothing in the project was tuned on. `alphafe eval`
loads every `*.jsonl` file here and reports the results as a separate suite
called `real`. The directory is empty until someone compiles it. That is your
task.

The result is only worth something if the problems are chosen without regard
to whether the solver can do them. Most of the rules below exist to protect
that.

## What to deliver

1. `benchmarks/real/real.jsonl`: one problem per line, in the format below.
2. `benchmarks/real/SKIPPED.md`: the selection rule you used, and every
   problem you considered and left out, with the reason.
3. `scripts/validate_bench.py` exits with no errors, and the test suite passes.
4. One or more commits. Do not push.

Do not add anything else. In particular, do not edit `alphafe/`, `tests/`,
`benchmarks/seed/` or `benchmarks/synthetic/` to make a problem fit. If the
validator or a test seems wrong, stop and report it.

## Rules

1. Open a source for every problem. Record the URL you opened in the `url`
   field and copy the problem statement from it into `statement`. Never write
   a problem, an answer or a citation from memory. If you cannot open a
   source for a problem, leave the problem out.
2. Do not change a problem to make it fit. Do not change the domain, drop a
   hypothesis, strengthen a condition or simplify the equation. A problem
   that does not fit as stated goes in `SKIPPED.md`.
3. Decide the selection rule first and write it at the top of `SKIPPED.md`
   before collecting anything. A good rule names sources and takes everything
   in scope from them, for example "every functional equation in contests A,
   B and C from 2000 to 2024". Do not pick problems one by one.
4. Do not run the solver on a problem before `real.jsonl` and `SKIPPED.md`
   are committed. Never remove or replace a problem because the solver fails
   on it, and never add one because the solver succeeds.
5. Nothing in this directory may be used for training, for choosing
   hyperparameters or for deciding which fix to keep. The synthetic generator
   excludes these problems from future training pools by a hash of the
   equation, so you do not need to do anything for that.
6. Use the project virtual environment for every command
   (`.venv/bin/python`, `.venv/bin/alphafe`). Do not install packages
   globally. Setup is in the README.

## Which problems are in scope

Version 1 of the solver handles a narrow class. A problem is in scope only if
every line of this list holds for the problem exactly as its source states it.

* It asks for all functions f satisfying one equation.
* There is one unknown function, from R to R or from Q to Q.
* The equation holds for all values of one, two or three variables.
* The equation is built from the variables, rational constants, `+`, `-`,
  `*`, non-negative integer powers, and f applied to such expressions.
* There is no other hypothesis: no continuity, monotonicity, boundedness,
  injectivity, no given value such as f(1) = 1, no second equation, no
  inequality.
* Every solution is a polynomial with rational coefficients, and the full
  answer is a finite list of families in which the free constants range over
  the whole domain and enter linearly, such as `f(x) = cx + d`.

Out of scope, with examples of what to write in `SKIPPED.md`:

| problem as stated | reason |
|---|---|
| f: R+ -> R+, or f on the integers or naturals | domain not supported |
| f: Q -> R, or f: R -> R≥0 | domain and codomain differ |
| "f is continuous", "f is increasing", "f(1) = 1" | extra hypothesis |
| f(x/y), or 1/x anywhere | division by a variable |
| two unknown functions, or two equations | not a single equation in one function |
| an inequality, or "prove that f is ..." | not "find all f satisfying an equation" |
| four or more variables | too many variables |
| answer contains abs(x), 1/x, a floor, a piecewise rule or sqrt(2) | answer is not a rational polynomial |
| Cauchy's equation over R with no regularity condition | non-polynomial solutions exist |
| answer is "f(x) = cx with c ≥ 0" or "c ≠ 0" | restricted parameter cannot be recorded |
| same equation as a seed or held-out synthetic problem | duplicate (the validator reports these) |

A restriction to finitely many values is fine: write "f(x) = cx with c = 0 or
c = 1" as two entries, `f(x) = 0` and `f(x) = x`.

Out-of-scope problems are not failures of yours. A selection rule applied to
real contests will skip most functional equations, and `SKIPPED.md` is where
that shows.

### Where to look

These are starting points. Check that each link opens before relying on it,
and prefer the official or most direct source for each problem.

* Official contest pages, such as the IMO problems archive at
  https://www.imo-official.org/problems.aspx.
* The Art of Problem Solving contest collections at
  https://artofproblemsolving.com/community/c13_contests, which carry
  statements for national and regional olympiads.
* Evan Chen's MOHS ratings at https://web.evanchen.cc/upload/MOHS-hardness.pdf,
  which rate many recent olympiad problems on the scale this project uses.

The solver's target range is 0M to 10M on the MOHS scale. IMO-level contests
have few functional equations that easy, so a rule that covers national
olympiads, junior rounds and regional contests will yield more in-scope
problems. Include the harder in-scope problems from your sources too; do not
cut the list at a difficulty.

Unless you were told a number, aim for at least 30 problems in `real.jsonl`.
If your rule yields fewer, widen the rule (more contests or years) and record
the wider rule; do not start hand-picking.

## Record format

`real.jsonl` is JSON Lines: one JSON object per line. Blank lines and lines
starting with `#` are ignored. The line below shows the format only. It is a
made-up problem and must not be copied into the file.

```json
{"id": "example-2000-1", "equation": "f(x + 3y) = f(x) + 3y", "domain": "R", "solutions": ["f(x) = x + c"], "mohs": 0, "mohs_source": "estimate", "source": "Example Olympiad 2000, Problem 1", "url": "https://example.org/2000/problem1", "statement": "Find all functions f: R -> R such that f(x + 3y) = f(x) + 3y for all real numbers x and y."}
```

All nine fields are required.

| field | content |
|---|---|
| `id` | unique short name: lowercase letters, digits and hyphens, such as `usamo-2002-4` |
| `equation` | the equation in the syntax below |
| `domain` | `"R"` or `"Q"`; the codomain is the same set |
| `solutions` | the complete answer as a list of strings; `[]` if no function satisfies the equation |
| `mohs` | difficulty on the MOHS scale: one of 0, 5, 10, ..., 50 |
| `mohs_source` | `"chen"` if the number is Evan Chen's published rating for this problem, otherwise `"estimate"` |
| `source` | contest, year and problem number |
| `url` | the page you opened to read the problem |
| `statement` | the problem statement as the source gives it, in plain text |

You may add other fields, for example `"notes"`. The loader keeps them and
ignores them.

### Equation syntax

* Variables are `x`, `y`, `z`. Rename the source's variables to these.
* The function is `f` and is always applied: `f(x + y)`, `f(f(x))`.
* Numbers are integers or fractions of integers: `2`, `1/2`. Decimals such as
  `0.5` are rejected.
* Operators are `+`, `-`, `*` and `^` with a non-negative integer exponent.
  Products may be written by juxtaposition: `2x`, `xy`, `xf(y)`, `f(x)f(y)`.
* Division is allowed only by an integer literal: `x/2`.
* Exactly one `=`. No other letters: `f(a + b)` is rejected.

Rewriting that keeps the problem the same is expected: renaming variables,
writing the source's notation in this syntax, expanding a constant. Anything
that changes which functions satisfy the equation is not allowed.

### Answer syntax

* Each entry is `f(x) = ` followed by a polynomial in `x`, in the same syntax
  as equations: `f(x) = 0`, `f(x) = x^2`, `f(x) = x/2 + 1/3`.
* Free constants are written with the letters `a b c d e g h k m n p q r s`.
  The letters `t u v w y z` are read as variables and rejected.
  `f(x) = c*x + d` means "for any constants c and d in the domain".
* Entries are independent. The same letter in two entries names two unrelated
  constants.
* List each family once. `["f(x) = c*x", "f(x) = 0"]` gets a warning because
  the second entry is already covered by the first.

The answer must be the complete solution set from a published solution. Read
the official or a well-checked solution and record exactly its answer. If
sources disagree about the answer, leave the problem out and say so in
`SKIPPED.md`.

### Difficulty

If Evan Chen's chart rates the problem, use that number and set `mohs_source`
to `"chen"`. Otherwise estimate on the same scale and set it to `"estimate"`.
For calibration: 0M is a problem a single substitution solves, 5M to 10M
takes a few standard steps, and 30M is a medium-hard IMO problem. An estimate
is a rough label; do not spend long on it.

## `SKIPPED.md`

Start with the selection rule, then a table of every problem the rule covered
that is not in `real.jsonl`:

```markdown
# Selection rule

Every functional equation in <contests> from <year> to <year>, read from <where>.

# Skipped

| problem | url | reason |
|---|---|---|
| Example Olympiad 2001, Problem 3 | https://example.org/2001/problem3 | f: R+ -> R+ |
```

End with the counts: problems covered by the rule, in scope, skipped.

## Checking your work

```sh
.venv/bin/python scripts/validate_bench.py
```

This checks every `*.jsonl` file in this directory and exits with status 1 if
there is an error. Fix every error. Read every warning and fix it unless you
have a reason not to.

| message | what to do |
|---|---|
| `missing fields` | add them; all nine are required |
| `equation or domain not accepted` | fix the syntax; if the problem cannot be written in the syntax it is out of scope |
| `solution ... does not satisfy the equation` | the answer or the equation is transcribed wrongly; go back to the source |
| `the answer is incomplete: ... also satisfies the equation` | the script found a polynomial solution of degree at most 2 that your answer does not list; go back to the source |
| `parameters must enter linearly` | the family cannot be recorded; the problem is out of scope |
| `same equation as seed problem` or `held-out synthetic problem` | move the problem to `SKIPPED.md` as a duplicate |
| `same equation as seed problem ..., over Q there` (warning) | the seed set has this equation on the other domain; keep the problem |
| `id already used` | choose another id |
| `note: ... also produced by the synthetic training generator` | keep the problem and add `"in_training_pool": true` to its record |

The last message is about the network weights published before this
benchmark existed. Their training pool could not exclude problems that were
not here yet, so a very simple real problem may coincide with one they
trained on. Such problems stay in the file, flagged, so that results can be
reported with and without them.

The validator proves less than it may seem to. It confirms that the listed
functions satisfy the equation, and that no polynomial of degree at most 2 is
missing. It cannot tell whether the answer is complete beyond that, or
whether the equation matches the source. Those depend on your reading of the
source, which is why `url` and `statement` are required.

Then run the tests:

```sh
.venv/bin/python -m pytest
```

Commit `real.jsonl` and `SKIPPED.md` together once both pass.

## After the commit

Running the solver is a separate step and may not be part of your task. If
you are asked to do it:

```sh
.venv/bin/alphafe eval --checkpoint checkpoints/best.pt --tag real --seeds 3 --big-budget 2000
```

This evaluates all benchmarks and writes tables to `results/`. Without a
checkpoint it still runs brute force.

If evaluation stops with `AnswerMismatch`, the checker accepted a proof whose
answer differs from the one recorded. Either the recorded answer is wrong or
the checker is unsound, and the second would be a serious bug. Do not edit
the answer to match. Re-read the source. If the source confirms the recorded
answer, stop and report the problem id, the equation and both answers. If you
mis-transcribed, fix the record, say so in the commit message, and run the
evaluation again.

Report the results for every problem in the file. Unsolved problems stay.

## What to report when you finish

* The selection rule and the three counts from `SKIPPED.md`.
* How many problems came from each source and how many at each MOHS value.
* Any problem flagged `in_training_pool`.
* Anything in these instructions or in the validator that was wrong or
  unclear.
