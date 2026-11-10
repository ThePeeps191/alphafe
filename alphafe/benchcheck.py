"""Checks for benchmark files, used by scripts/validate_bench.py.

What it can check: that every record is well formed, that the equation and
the answer parse, that every listed function satisfies the equation exactly,
that no polynomial solution of degree at most 2 is missing from the answer,
and that a problem does not duplicate one in another benchmark.

What it cannot check: that the answer is complete beyond polynomials of
degree 2, and that the equation was transcribed faithfully from its source.
Those two rest on whoever compiled the file.
"""

from __future__ import annotations

import json
import pathlib
import re
from dataclasses import dataclass, field

from . import terms as T
from .baseline.guesser import guess
from .bench import BENCH_DIR
from .checker import Problem
from .generate import canonical_key
from .solutions import make_family, parse_solution, verify

# Fields every record of the real benchmark must have (see benchmarks/real/INSTRUCTIONS.md).
REAL_FIELDS = ("id", "equation", "domain", "solutions", "mohs", "mohs_source", "source", "url", "statement")
BASIC_FIELDS = ("id", "equation", "domain")
ID_PATTERN = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
MOHS_SOURCES = ("chen", "estimate")


@dataclass
class Report:
    records: int = 0
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def read_records(path) -> list:
    """[(label, record or None, error text)] for every non-comment line of a JSON Lines file."""
    out = []
    path = pathlib.Path(path)
    for number, line in enumerate(path.read_text().splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        label = f"{path.name}:{number}"
        try:
            record = json.loads(line)
        except json.JSONDecodeError as err:
            out.append((label, None, f"not valid JSON ({err.msg})"))
            continue
        if not isinstance(record, dict):
            out.append((label, None, "each line must be a JSON object"))
            continue
        out.append((label, record, ""))
    return out


def other_benchmarks(skip=()) -> dict:
    """{canonical key: (benchmark name, id, domain)} for the seed set and the frozen held-out set."""
    skip = {pathlib.Path(p).resolve() for p in skip}
    known = {}
    for path in sorted((BENCH_DIR / "seed").glob("*.jsonl")):
        if path.resolve() in skip:
            continue
        for _, record, _ in read_records(path):
            if record:
                problem = Problem.parse(record["equation"], record.get("domain", "R"))
                known.setdefault(canonical_key(problem.poly), ("seed", record["id"], problem.domain))
    heldout = BENCH_DIR / "synthetic" / "heldout.jsonl"
    if heldout.exists() and heldout.resolve() not in skip:
        for _, record, _ in read_records(heldout):
            if record:
                known.setdefault(record["key"], ("held-out synthetic", record["id"], record.get("domain", "R")))
    return known


def check_record(record: dict, strict: bool) -> tuple:
    """(errors, warnings, canonical key or None) for one record on its own."""
    errors, warnings = [], []
    required = REAL_FIELDS if strict else BASIC_FIELDS
    missing = [name for name in required if name not in record]
    if missing:
        errors.append(f"missing field{'s' if len(missing) > 1 else ''}: {', '.join(missing)}")

    ident = record.get("id")
    if "id" in record and not (isinstance(ident, str) and ID_PATTERN.fullmatch(ident)):
        errors.append("id must be lowercase letters, digits and single hyphens, e.g. usamo-2002-4")

    for name in ("source", "url", "statement"):
        if name in record and not (isinstance(record[name], str) and record[name].strip()):
            errors.append(f"{name} must be a non-empty string")
    if strict and isinstance(record.get("url"), str) and not record["url"].startswith(("http://", "https://")):
        errors.append("url must be a link that was opened, starting with http:// or https://")

    if "mohs" in record:
        mohs = record["mohs"]
        if not (isinstance(mohs, int) and not isinstance(mohs, bool) and 0 <= mohs <= 50 and mohs % 5 == 0):
            errors.append("mohs must be one of 0, 5, 10, ..., 50")
    if "mohs_source" in record and record["mohs_source"] not in MOHS_SOURCES:
        errors.append(f"mohs_source must be one of: {', '.join(MOHS_SOURCES)}")

    problem = None
    if "equation" in record and "domain" in record:
        try:
            problem = Problem.parse(record["equation"], record["domain"])
        except (ValueError, TypeError, AttributeError) as err:     # ParseError is a ValueError
            errors.append(f"equation or domain not accepted: {err}")
    if problem is None:
        return errors, warnings, None

    extra = sorted(set(problem.poly.variables()) - set("xyz"))
    if extra:
        warnings.append(f"uses variable{'s' if len(extra) > 1 else ''} {', '.join(extra)}; rename to x, y, z")

    if "solutions" in record:
        errors_before = len(errors)
        families = _check_solutions(record["solutions"], problem, errors, warnings)
        if families is not None and len(errors) == errors_before:
            _check_against_polynomial_guess(problem, families, errors, warnings)
    return errors, warnings, canonical_key(problem.poly)


def _check_solutions(solutions, problem: Problem, errors: list, warnings: list):
    if not isinstance(solutions, list) or not all(isinstance(s, str) for s in solutions):
        errors.append('solutions must be a list of strings such as ["f(x) = c*x"]; use [] for no solutions')
        return None
    families = []
    for text in solutions:
        try:
            expr = parse_solution(text)
        except T.ParseError as err:
            errors.append(f"solution '{text}' not accepted: {err}")
            continue
        if not verify(problem.poly, expr):
            errors.append(f"solution '{text}' does not satisfy the equation")
            continue
        family = make_family(expr)
        if family.n_params and family.affine is None:
            errors.append(f"solution '{text}': parameters must enter linearly (a family such as c^2*x "
                          "or one with a restricted parameter cannot be recorded)")
            continue
        families.append((text, family))
    for i, (text, family) in enumerate(families):
        for j, (other_text, other) in enumerate(families):
            if i != j and other.contains(family) and not (family.contains(other) and i < j):
                warnings.append(f"solution '{text}' is already covered by '{other_text}'")
                break
    return [family for _, family in families]


def _check_against_polynomial_guess(problem: Problem, families: list, errors: list, warnings: list) -> None:
    """Every polynomial solution of degree <= 2 must be in the recorded answer."""
    found = guess(problem)
    if found.solutions is None:
        warnings.append("could not solve for the polynomial solutions of degree <= 2, so that check was skipped")
        return
    for fam in found.solutions.families:
        if not any(mine.contains(fam) for mine in families):
            errors.append(f"the answer is incomplete: {fam.describe()} also satisfies the equation")


def validate(paths, strict: bool = True, known: dict | None = None) -> Report:
    """Check benchmark files together (ids and equations must be unique across them)."""
    report = Report()
    paths = [pathlib.Path(p) for p in paths]
    known = dict(other_benchmarks(skip=paths) if known is None else known)
    seen_ids: dict = {}
    for path in paths:
        for label, record, problem_text in read_records(path):
            report.records += 1
            if record is None:
                report.errors.append(f"{label}: {problem_text}")
                continue
            name = f"{label} ({record.get('id', '?')})"
            errors, warnings, key = check_record(record, strict)
            ident = record.get("id")
            if isinstance(ident, str):
                if ident in seen_ids:
                    errors.append(f"id already used at {seen_ids[ident]}")
                seen_ids.setdefault(ident, label)
            if key is not None:
                if key in known:
                    where, other_id, other_domain = known[key]
                    text = f"same equation as {where} problem {other_id}"
                    if where == "seed" and other_domain != record.get("domain"):
                        warnings.append(f"{text}, over {other_domain} there")
                    elif not strict:
                        warnings.append(f"{text} up to renaming the variables")
                    else:
                        errors.append(f"{text} up to renaming the variables: leave it out and list it in SKIPPED.md")
                else:
                    known[key] = ("seed" if not strict else "real", ident, record.get("domain"))
            report.errors += [f"{name}: {e}" for e in errors]
            report.warnings += [f"{name}: {w}" for w in warnings]
    return report


def in_training_pool(paths, seed: int = 0, per_tier: int = 3000) -> list:
    """Ids of problems that the synthetic generator also produces for training.

    The published checkpoints were trained before any real problem existed,
    so the exclusion by canonical hash did not cover them. This regenerates
    the default training pool the way those runs did (excluding only the seed
    benchmark) and reports the overlap. It is a close reconstruction and not
    a record of what a past run saw: the generator's output can shift when
    the checker changes.
    """
    from .bench import load_seed
    from .generate import generate

    seed_keys = {canonical_key(b.problem.poly) for b in load_seed()}
    pool = generate(seed, per_tier, exclude=seed_keys)
    train_keys = {g.key for items in pool.values() for g in items if g.split == "train"}
    out = []
    for path in paths:
        for _, record, _ in read_records(path):
            if not record:
                continue
            try:
                problem = Problem.parse(record["equation"], record["domain"])
            except (KeyError, ValueError, TypeError, AttributeError):
                continue
            if canonical_key(problem.poly) in train_keys:
                out.append(record.get("id", "?"))
    return out
