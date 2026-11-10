"""Checks for benchmark files, used by scripts/validate_bench.py.

What it can check: that every record is well formed, that the equation and
the answer parse, that every listed function satisfies the equation exactly,
that no polynomial solution of degree at most 2 is missing from the answer,
that no listed family of higher degree is missing a quadratic, linear or
constant term, and that a problem does not duplicate one in another benchmark.

What it cannot check: that the answer is complete beyond that, and that the
equation was transcribed faithfully from its source. Those two rest on
whoever compiled the file. When one of the completeness checks cannot be
carried out for a record, the report says so in a note.
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
from .algebra import Unsupported, parse_poly
from .solutions import X, fit_candidate, make_family, make_solution_set, parse_solution, verify

# Fields every record of the real benchmark must have (see benchmarks/real/INSTRUCTIONS.md).
REAL_FIELDS = ("id", "equation", "domain", "solutions", "mohs", "mohs_source", "source", "url", "statement")
BASIC_FIELDS = ("id", "equation", "domain")
ID_PATTERN = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
MOHS_SOURCES = ("chen", "estimate")
# Substituting a quadratic into an equation with an exponent n gives a polynomial of degree 2n whose
# expansion takes seconds at n = 50 and does not finish at n = 2000, so above this the check is skipped.
MAX_CHECK_EXPONENT = 40


@dataclass
class Report:
    records: int = 0
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    notes: list = field(default_factory=list)      # checks that could not be carried out; nothing to fix

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


def max_exponent(term: T.Term) -> int:
    """The largest exponent in a term, nested powers multiplied: ((x^2)^3 counts as 6)."""
    if isinstance(term, T.Pow):
        return term.exp * max(1, max_exponent(term.base))
    if isinstance(term, (T.Add, T.Sub, T.Mul)):
        return max(max_exponent(term.left), max_exponent(term.right))
    if isinstance(term, (T.Neg, T.App)):
        return max_exponent(term.arg)
    return 1


def check_record(record: dict, strict: bool) -> tuple:
    """(errors, warnings, notes, canonical key or None) for one record on its own.

    Errors must be fixed and warnings should be. A note reports a
    completeness check that could not be carried out for this record; there
    is nothing to fix, but the recorded answer then rests on the source alone.
    """
    errors, warnings, notes = [], [], []
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
        return errors, warnings, notes, None

    extra = sorted(set(problem.poly.variables()) - set("xyz"))
    if extra:
        warnings.append(f"uses variable{'s' if len(extra) > 1 else ''} {', '.join(extra)}; rename to x, y, z")

    if "solutions" in record:
        errors_before = len(errors)
        families = _check_solutions(record["solutions"], problem, errors, warnings)
        if families is not None and len(errors) == errors_before:
            exponent = max(max_exponent(side) for side in T.parse_equation(record["equation"]))
            if exponent > MAX_CHECK_EXPONENT:
                notes.append(f"the equation has an exponent of {exponent} (above {MAX_CHECK_EXPONENT}), so the search "
                             "for polynomial solutions missing from the answer was skipped")
            else:
                _check_against_polynomial_guess(problem, families, errors, notes)
                _check_around_families(problem, families, errors, notes)
    return errors, warnings, notes, canonical_key(problem.poly)


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


def _check_against_polynomial_guess(problem: Problem, families: list, errors: list, notes: list) -> None:
    """Every polynomial solution of degree <= 2 must be in the recorded answer."""
    found = guess(problem)
    if found.solutions is None:
        notes.append("could not solve for the polynomial solutions of degree <= 2, so that check was skipped")
        return
    if found.skipped:
        notes.append(f"missing solutions were searched for among {found.template} functions only: the coefficient "
                     f"system for {' and '.join(found.skipped)} functions could not be solved exactly")
    for fam in found.solutions.families:
        if not any(mine.contains(fam) for mine in families):
            errors.append(f"the answer is incomplete: {fam.describe()} also satisfies the equation")


def _check_around_families(problem: Problem, families: list, errors: list, notes: list) -> None:
    """A recorded family of degree 3 or more must not be missing a term of degree <= 2.

    The check above fits a*x^2 + b*x + c on its own, which says nothing near a
    cubic: if the full answer is x^3 + c*x and only x^3 is recorded, no
    quadratic satisfies the equation and nothing is reported. So each such
    family g is refitted as g + a*x^2 + b*x + e with fresh constants.
    """
    for family in families:
        if max(family.expr.coeffs_in(X), default=0) <= 2:
            continue
        try:
            fits = fit_candidate(problem.poly, family.expr + parse_poly("a*x^2 + b*x + e"), problem.domain)
        except Unsupported:
            notes.append(f"could not test whether {family.describe()} is missing a term of degree <= 2")
            continue
        for found in make_solution_set(fits).families:
            if not any(mine.contains(found) for mine in families):
                errors.append(f"the answer is incomplete: {found.describe()} also satisfies the equation")


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
            errors, warnings, notes, key = check_record(record, strict)
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
            report.notes += [f"{name}: {n}" for n in notes]
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
