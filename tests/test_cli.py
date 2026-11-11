from alphafe.cli import main


def test_solve_with_baseline(capsys):
    code = main(["solve", "f(x+y) = f(x) + y", "--baseline"])
    out = capsys.readouterr().out
    assert code == 0
    assert "Answer. f(x) = x + c for any constant c." in out
    # The opening substitutions are applied by the environment itself, so no search runs on this problem.
    assert "Found by: the routine moves alone, without search" in out and "P(0, y)" in out
    code = main(["solve", "f(x)f(y) = f(x+y) + xy", "--baseline"])       # this one needs a case split
    assert code == 0 and "Found by: baseline" in capsys.readouterr().out


def test_solve_reports_failure_honestly(capsys):
    code = main(["solve", "f(x+y) = f(x) + f(y)", "--domain", "R", "--baseline", "--baseline-budget", "200"])
    out = capsys.readouterr().out
    assert code == 1 and "No proof found" in out and "Answer." not in out


def test_solve_without_checkpoint_falls_back(capsys, tmp_path):
    code = main(["solve", "f(xy) = x*f(y)", "--checkpoint", str(tmp_path / "missing.pt")])
    out = capsys.readouterr().out
    assert code == 0 and "No checkpoint" in out and "f(x) = cx" in out


def test_check_accepts_and_rejects(capsys, tmp_path):
    good = tmp_path / "good.proof"
    good.write_text("sub P: x:=0\nconclude\n")
    assert main(["check", "f(x+y) = f(x) + y", "--proof", str(good)]) == 0
    assert "solved: f(x) = x + c" in capsys.readouterr().out
    bad = tmp_path / "bad.proof"
    bad.write_text("cancel\n")
    assert main(["check", "f(x+y) = f(x)", "--proof", str(bad), "--quiet"]) == 1
    assert "rejected at move 1" in capsys.readouterr().out


# --- malformed input: one line on stderr and exit status 2, never a traceback ---------------------------------

BAD_EQUATIONS = [
    ("f(x+y) = ", "unexpected end of input"),
    ("f(x+y) = f(x) + 0.5y", "unexpected character"),
    ("f(x)/x = 1", "division is only allowed by an integer literal"),
    ("f = x", "must be applied"),
    ("f(x+y+z+t) = f(x) + y + z + t", "4 variables"),
    ("g(x+y) = g(x) + y", "also uses g"),
    ("f(x) = f(x)", "holds for every function"),
    ("x + y = y + x", "holds for every function"),
    ("f(1) = 2", "at least one variable"),
    ("x + y = 2", "does not involve f"),
]


def test_malformed_equations_exit_with_status_2_and_one_line(capsys):
    for equation, message in BAD_EQUATIONS:
        for command in (["solve", equation, "--baseline"], ["check", equation, "--proof", "-"]):
            assert main(command) == 2, equation
            captured = capsys.readouterr()
            assert captured.err.startswith("alphafe: error: ") and message in captured.err, (equation, captured.err)
            assert captured.err.count("\n") == 1 and "Traceback" not in captured.err


def test_bad_proof_files_name_the_line(capsys, tmp_path):
    assert main(["check", "f(x+y) = f(x) + y", "--proof", str(tmp_path / "missing.proof")]) == 2
    assert "alphafe: error:" in capsys.readouterr().err
    for text, message in [("sub P: x:=0\nsub P: q:=1\n", "line 2: 'sub P: q:=1': bad binding"),
                          ("# a comment\n\nfrobnicate R1\n", "line 3: 'frobnicate R1': unknown move")]:
        path = tmp_path / "bad.proof"
        path.write_text(text)
        assert main(["check", "f(x+y) = f(x) + y", "--proof", str(path)]) == 2
        assert message in capsys.readouterr().err


def test_a_rejected_proof_and_no_proof_found_keep_status_1(capsys, tmp_path):
    proof = tmp_path / "p.proof"
    proof.write_text("cancel\n")
    assert main(["check", "f(x+y) = f(x)", "--proof", str(proof), "--quiet"]) == 1
    assert main(["solve", "f(x+y) = f(x) + f(y)", "--baseline", "--baseline-budget", "50"]) == 1
    capsys.readouterr()


def test_unknown_device_is_refused_by_the_argument_parser(capsys):
    import pytest

    with pytest.raises(SystemExit) as stop:
        main(["solve", "f(x+y) = f(x) + y", "--device", "bogus"])
    assert stop.value.code == 2 and "invalid choice" in capsys.readouterr().err


def test_a_corrupt_checkpoint_falls_back_to_brute_force(capsys, tmp_path):
    import pytest

    pytest.importorskip("torch")
    for name, content in (("garbage.pt", bytes(range(256)) * 8), ("empty.pt", b"")):
        path = tmp_path / name
        path.write_bytes(content)
        assert main(["solve", "f(x+y) = f(x) + y", "--checkpoint", str(path), "--device", "cpu"]) == 0
        out = capsys.readouterr().out
        assert "Could not load" in out and "using the brute-force baseline" in out and "Answer. f(x) = x + c" in out


# --- variables other than x, y, z ------------------------------------------------------------------------------

def test_other_variable_letters_are_renamed(capsys):
    assert main(["solve", "f(t+u) = f(t) + u", "--baseline"]) == 0
    out = capsys.readouterr().out
    assert "Variables renamed to x, y, z: t -> x, u -> y." in out
    assert "find all f: R -> R with f(x + y) = f(x) + y" in out and "Answer. f(x) = x + c" in out
    # Nothing is said when there is nothing to rename.
    assert main(["solve", "f(x+y) = f(x) + y", "--baseline"]) == 0
    assert "renamed" not in capsys.readouterr().out
