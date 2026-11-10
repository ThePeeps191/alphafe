"""Hypothesis strategies shared by the test suite."""

from fractions import Fraction

from hypothesis import strategies as st

from alphafe import terms as T

small_ints = st.integers(min_value=-4, max_value=4)
small_fracs = st.builds(Fraction, small_ints, st.integers(min_value=1, max_value=3))

leaves = st.one_of(
    st.sampled_from([T.Var("x"), T.Var("y"), T.Var("z")]),
    st.sampled_from([T.Sym("a"), T.Sym("b")]),
    small_fracs.map(T.Num),
)


def _extend(children):
    return st.one_of(
        st.builds(T.Add, children, children),
        st.builds(T.Sub, children, children),
        st.builds(T.Mul, children, children),
        st.builds(T.Neg, children),
        st.builds(T.App, children),
        st.builds(T.Pow, children, st.integers(min_value=0, max_value=2)),
    )


terms = st.recursive(leaves, _extend, max_leaves=6)
