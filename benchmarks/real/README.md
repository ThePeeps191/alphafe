# Real benchmark problems

This directory is intentionally empty. The project owners add hand-picked
problems here; `alphafe eval` picks up every `*.jsonl` file automatically.
Nothing in this directory is ever used for training.

## File format

One JSON object per line:

```json
{"id": "usamo-2002-4", "equation": "f(x^2 - y^2) = x*f(x) - y*f(y)", "domain": "R", "solutions": ["f(x) = c*x"], "mohs": 10, "source": "USAMO 2002/4"}
```

| field       | meaning |
|-------------|---------|
| `id`        | unique short name |
| `equation`  | the equation in plain text; variables are `x y z`, the function is `f` |
| `domain`    | `"R"` or `"Q"` (domain and codomain are the same) |
| `solutions` | the full expected solution set, each written `f(x) = ...`; letters other than `x` are free parameters. Use `[]` for "no solutions" and omit the field if the answer is unknown |
| `mohs`      | estimated difficulty on Evan Chen's MOHS scale (0, 5, 10, ...) |
| `source`    | where the problem comes from |

Syntax: `+ - *`, integer powers `^`, juxtaposition for products (`2x`, `xf(y)`),
and division by integer literals only (`x/2`).
