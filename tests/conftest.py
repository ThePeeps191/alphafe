import pytest


@pytest.fixture
def plain_environment(monkeypatch):
    """Switch off the routine substitutions of ``alphafe.env`` (opening moves, swap, instances, witnesses).

    Tests of the search, the tokenizer and the training code use very easy
    problems as their subjects. With the routine substitutions on, the
    environment solves those before any search runs, and the test would no
    longer exercise what it is about. The routine substitutions have their
    own tests in tests/test_routine.py.
    """
    from alphafe import env

    for name in env.ROUTINE:
        monkeypatch.setitem(env.ROUTINE, name, False)
