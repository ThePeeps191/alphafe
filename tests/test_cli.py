from alphafe.cli import main


def test_solve_with_baseline(capsys):
    code = main(["solve", "f(x+y) = f(x) + y", "--baseline"])
    out = capsys.readouterr().out
    assert code == 0
    assert "Answer. f(x) = x + c for any constant c." in out
    assert "Found by: baseline" in out and "P(0, y)" in out


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
