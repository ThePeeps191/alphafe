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
    for g in ALL[::5]:
        state, _ = start(g.problem())
        assert not state.solved


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
