"""The baseline is the experimental control: training code must not touch it."""

import ast
import pathlib

PACKAGE = pathlib.Path(__file__).resolve().parent.parent / "alphafe"
TRAINING_MODULES = ["train.py", "selfplay.py", "model.py", "tokenizer.py", "generate.py", "policy.py"]


def imported_modules(path):
    names = set()
    for node in ast.walk(ast.parse(path.read_text())):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            names.add("." * node.level + (node.module or ""))
            names.update(alias.name for alias in node.names)
    return names


def test_training_code_never_imports_the_baseline():
    for name in TRAINING_MODULES:
        path = PACKAGE / name
        if not path.exists():
            continue
        for module in imported_modules(path):
            assert "baseline" not in module, f"{name} imports {module}"


def test_baseline_results_are_tagged():
    from alphafe.baseline.search import brute_force
    from alphafe.checker import Problem

    assert brute_force(Problem.parse("f(x+y) = f(x) + y"), max_calls=50).source == "baseline"
