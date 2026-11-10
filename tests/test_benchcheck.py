"""The benchmark validator: passes on the benchmarks in the repository and catches each kind of bad record."""

import json

from alphafe.bench import BENCH_DIR
from alphafe.benchcheck import REAL_FIELDS, check_record, validate

GOOD = {"id": "example-2000-1", "equation": "f(x + 3y) = f(x) + 3y", "domain": "R", "solutions": ["f(x) = x + c"],
        "mohs": 0, "mohs_source": "estimate", "source": "Example Olympiad 2000, Problem 1",
        "url": "https://example.org/2000/1", "statement": "Find all f: R -> R with f(x + 3y) = f(x) + 3y for all real x, y."}


def write(tmp_path, records, name="mine.jsonl"):
    path = tmp_path / name
    path.write_text("\n".join(r if isinstance(r, str) else json.dumps(r) for r in records) + "\n")
    return path


def errors_for(tmp_path, **changes):
    record = {k: v for k, v in {**GOOD, **changes}.items() if v is not None}
    return " | ".join(validate([write(tmp_path, [record])]).errors)


def test_the_real_benchmark_in_the_repository_is_valid():
    """Whatever is in benchmarks/real must pass the full check. (Passes trivially while it is empty.)"""
    report = validate(sorted((BENCH_DIR / "real").glob("*.jsonl")), strict=True)
    assert report.errors == []


def test_the_seed_benchmark_passes_the_basic_check():
    report = validate(sorted((BENCH_DIR / "seed").glob("*.jsonl")), strict=False)
    assert report.records == 50 and report.errors == []
    # Two pairs are the same equation with x and y exchanged; reported, not fatal, for the seed set.
    assert sum("up to renaming" in w for w in report.warnings) == 2


def test_a_good_record_passes(tmp_path):
    report = validate([write(tmp_path, ["# a comment", GOOD])])
    assert report.records == 1 and report.errors == [] and report.warnings == []


def test_every_real_field_is_required(tmp_path):
    for name in REAL_FIELDS:
        assert name in errors_for(tmp_path, **{name: None}), name


def test_wrong_and_incomplete_answers_are_errors(tmp_path):
    assert "does not satisfy" in errors_for(tmp_path, solutions=["f(x) = 2x"])
    assert "incomplete" in errors_for(tmp_path, solutions=["f(x) = x"])
    assert "incomplete" in errors_for(tmp_path, solutions=[])
    assert "list of strings" in errors_for(tmp_path, solutions="f(x) = x + c")


def test_answer_syntax_errors(tmp_path):
    assert "written in the variable x" in errors_for(tmp_path, solutions=["f(x) = x + t"])
    assert "f(x) = ..." in errors_for(tmp_path, solutions=["f(y) = y + c"])
    # f(x) = c^2 x^2 solves f(x)f(y) = f(xy)... only for c^2 in {0, 1}; a nonlinear parameter that does verify:
    errors, _, _, _ = check_record({**GOOD, "equation": "f(x + y) = f(x) + f(y)", "domain": "Q",
                                    "solutions": ["f(x) = c^2*x"]}, strict=True)
    assert any("enter linearly" in e for e in errors)


def test_field_format_errors(tmp_path):
    assert "id must be" in errors_for(tmp_path, id="USAMO_2002")
    assert "mohs must be" in errors_for(tmp_path, mohs=7)
    assert "mohs must be" in errors_for(tmp_path, mohs="10")
    assert "mohs_source" in errors_for(tmp_path, mohs_source="guess")
    assert "url must be" in errors_for(tmp_path, url="from memory")
    assert "not accepted" in errors_for(tmp_path, equation="f(a + b) = f(a) + b")
    assert "not accepted" in errors_for(tmp_path, domain="R+")
    assert "not valid JSON" in " ".join(validate([write(tmp_path, ["{oops"])]).errors)


def test_duplicates_are_errors(tmp_path):
    again = {**GOOD, "id": "example-2000-2", "equation": "f(y + 3x) = f(y) + 3x"}       # variables exchanged
    report = validate([write(tmp_path, [GOOD, again, {**GOOD, "equation": "f(x + 4y) = f(x) + 4y"}])])
    text = " | ".join(report.errors)
    assert "same equation as real problem example-2000-1" in text and "id already used" in text
    assert "same equation as seed problem s01" in errors_for(tmp_path, equation="f(x + y) = f(x) + y")
    heldout = json.loads((BENCH_DIR / "synthetic" / "heldout.jsonl").read_text().splitlines()[0])
    assert "held-out synthetic" in errors_for(tmp_path, equation=heldout["equation"], domain=heldout["domain"],
                                               solutions=[heldout["planted"]])


def test_warnings_do_not_fail_the_check(tmp_path):
    record = {**GOOD, "equation": "f(u + 3v) = f(u) + 3v", "solutions": ["f(x) = x + c", "f(x) = x"]}
    report = validate([write(tmp_path, [record])])
    assert report.ok and len(report.warnings) == 2


def notes_for(tmp_path, **changes):
    report = validate([write(tmp_path, [{**GOOD, **changes}])])
    return report, " | ".join(report.notes)


def test_a_cubic_answer_missing_its_lower_terms_is_an_error(tmp_path):
    """No quadratic satisfies these equations, so only a fit around the recorded cubic can see the gap."""
    assert "incomplete" in errors_for(tmp_path, equation="f(x + y) = f(x) + f(y) + 3xy(x + y)", domain="Q",
                                      solutions=["f(x) = x^3"])
    assert "incomplete" in errors_for(tmp_path, equation="(x - y)f(x + y) - (x + y)f(x - y) = 8xy(x^2 - y^2)",
                                      solutions=["f(x) = 2x^3"])
    assert errors_for(tmp_path, equation="f(x + y) = f(x) + f(y) + 3xy(x + y)", domain="Q",
                      solutions=["f(x) = x^3 + c*x"]) == ""


def test_a_check_that_could_not_be_done_is_reported_in_a_note(tmp_path):
    # f(f(x)) = 2x has the solutions sqrt(2)x and -sqrt(2)x: the linear system has no exact solution,
    # so only constants were searched and the record must not pass silently.
    report, notes = notes_for(tmp_path, equation="f(f(x)) = 2x", solutions=[])
    assert report.ok and "among constant functions only" in notes
    # A complete search leaves no note.
    report, notes = notes_for(tmp_path)
    assert report.ok and notes == ""


def test_a_huge_exponent_skips_the_polynomial_search_instead_of_hanging(tmp_path):
    """Substituting a quadratic into a 2015th power does not finish; the validator says it skipped the check."""
    report, notes = notes_for(tmp_path, equation="f(x^2015 + f(y)^2015) = f(x)^2015 + y^2015",
                              solutions=["f(x) = x", "f(x) = -x"])
    assert report.ok and "exponent of 2015" in notes
    # The listed functions are still verified by substitution.
    assert "does not satisfy" in errors_for(tmp_path, equation="f(x^2015 + f(y)^2015) = f(x)^2015 + y^2015",
                                            solutions=["f(x) = 2x"])


def test_max_exponent_multiplies_nested_powers():
    from alphafe import terms as T

    assert T.max_exponent(T.parse("f(x^3 + y)^2 + (x^2)^5")) == 10
    assert T.max_exponent(T.parse("f(x + y)")) == 1
