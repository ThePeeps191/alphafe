from alphafe.algebra import equation_poly
from alphafe.checker import verify_solution
from alphafe.env import start
from alphafe.generate import N_TIERS, benchmark_keys, canonical_key, generate, tier_of

DATA = generate(seed=3, per_tier=40, exclude=benchmark_keys())
ALL = [g for items in DATA.values() for g in items]


def test_every_tier_is_filled():
    assert set(DATA) == set(range(1, N_TIERS + 1))
    assert all(len(items) == 40 for items in DATA.values())


def test_generated_problems_are_valid_and_planted_solution_works():
    for g in ALL:
        problem = g.problem()
        assert len(problem.poly.variables()) == 2
        assert verify_solution(problem, g.planted), g.equation


def test_generated_problems_are_not_trivial():
    """The generator's promise: the free moves alone do not finish a generated problem.
    (The environment's routine substitutions may; training pools leave those problems out.)"""
    from alphafe.checker import initial_state
    from alphafe.env import close_free

    for g in ALL[::5]:
        state, _ = close_free(initial_state(g.problem()))
        assert not state.solved


def test_twins_of_benchmark_problems_are_protected():
    """A sign-flipped copy of a benchmark problem has another canonical key but is the same problem."""
    from alphafe.checker import Problem
    from alphafe.generate import protected_keys, twin_keys

    keys = protected_keys()
    assert benchmark_keys() <= keys
    for twin in ("f(x - y) + f(x) = 2x - y",       # seed s10 with y -> -y
                 "f(y)f(x) + f(xy) = x + y"):       # seed s22, f(x)f(y) = f(xy) + x + y, with f -> -f
        problem = Problem.parse(twin)
        assert twin_keys(problem.equation) & keys, twin
    assert canonical_key(Problem.parse("f(x - y) + f(x) = 2x - y").poly) not in benchmark_keys()  # the plain key misses it
    assert len(twin_keys("f(x + y) = f(x) + y")) <= 8


def test_no_duplicates_and_no_benchmark_problems():
    keys = [g.key for g in ALL]
    assert len(set(keys)) == len(keys)
    assert not set(keys) & benchmark_keys()


def test_generation_is_deterministic():
    again = generate(seed=3, per_tier=40, exclude=benchmark_keys())
    assert [g.equation for g in again[2]] == [g.equation for g in DATA[2]]
    other = generate(seed=4, per_tier=40, exclude=benchmark_keys())
    assert [g.equation for g in other[2]] != [g.equation for g in DATA[2]]


def test_split_is_a_function_of_the_problem_only():
    assert {g.split for g in ALL} == {"train", "test"}
    for g in ALL:
        assert g.split == ("test" if int(g.key[:8], 16) % 10 == 0 else "train")


def test_canonical_key_ignores_names_and_scaling():
    a = canonical_key(equation_poly("f(x + f(y)) = f(x) + y"))
    assert a == canonical_key(equation_poly("f(y + f(x)) = f(y) + x"))
    assert a == canonical_key(equation_poly("2f(x) + 2y = 2f(x + f(y))"))
    assert a != canonical_key(equation_poly("f(x + f(y)) = f(x) - y"))


def test_tiers_follow_structure_only():
    assert tier_of(1, 10) == 1 and tier_of(1, 30) == 2 and tier_of(2, 12) == 3 and tier_of(2, 30) == 4
    for g in ALL:
        assert g.tier == tier_of(g.depth, g.size)
    assert all(g.depth == 1 for g in DATA[1]) and all(g.depth >= 2 for g in DATA[3])


def test_a_disguised_problem_has_the_same_solutions_and_its_undo_moves_recover_the_plain_one():
    import random

    from alphafe.algebra import monic
    from alphafe.checker import apply, initial_state
    from alphafe.generate import disguise
    from alphafe.moves import parse_move

    rng = random.Random(4)
    made = {1: 0, 2: 0, 3: 0}
    for index, item in enumerate([g for items in DATA.values() for g in items][:120]):
        layers = 1 + index % 3
        hidden = disguise(item, rng, layers)
        if hidden is None:
            continue
        made[layers] += 1
        assert len(hidden.plan) == layers and hidden.undo == hidden.plan[0] and hidden.plain == item.equation
        assert hidden.planted == item.planted and hidden.key != item.key
        problem = hidden.problem()
        assert verify_solution(problem, hidden.planted), hidden.equation
        # The undo moves, applied in order by the plain checker, give the plain equation back.
        state = initial_state(problem)
        for text in hidden.plan:
            state = apply(state, parse_move(text))
        plain = monic(item.problem().poly)
        assert state.current.known_zero(plain), (item.equation, hidden.equation, hidden.plan)
    assert made[1] >= 20 and made[2] >= 10 and made[3] >= 5, made


def test_every_change_of_variables_is_undone_by_its_inverse():
    from alphafe.algebra import parse_poly
    from alphafe.generate import CHANGES, _renamed
    from alphafe.algebra import to_poly

    probe = parse_poly("f(x + 2y) + x*f(y) - 3x*y^2 + f(f(x) - y)")
    for _, change, inverse in CHANGES:
        for v, u in (("x", "y"), ("y", "x")):
            where = {"v": v, "u": u}
            forward = {where[name]: to_poly(_renamed(text, v, u)) for name, text in change.items()}
            back = {where[name]: to_poly(_renamed(text, v, u)) for name, text in inverse.items()}
            assert probe.subst(forward).subst(back) == probe, (change, inverse)
