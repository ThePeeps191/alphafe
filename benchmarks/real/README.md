# Real benchmark

Real competition problems, used only for testing. Nothing here is used for
training or for choosing between versions of the solver.

The directory holds no problems yet. `INSTRUCTIONS.md` describes how to
compile it: which problems are in scope, the file format, the rules that keep
the selection unbiased, and how to check the result with
`scripts/validate_bench.py`.

`alphafe eval` loads every `*.jsonl` file in this directory and reports it as
the `real` suite.
