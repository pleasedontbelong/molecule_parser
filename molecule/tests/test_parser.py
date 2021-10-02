import pytest
from molecule.parser import clean, multiply, parse


@pytest.mark.parametrize(
    "formula_str,expected",
    [
        ("A", "(A)1"),
        ("(A)", "(A)1"),
        ("(AB)2", "(AB)2"),
        ("(AB1)23", "(AB1)23"),
        ("A[B]", "(A(B)1)1"),
        ("{A[B]}2", "(A(B)1)2"),
        ("(A(B))", "(A(B)1)1"),
        ("(A(B)C)", "(A(B)1C)1"),
        ("ABC(DE)(FG)", "(ABC(DE)1(FG)1)1"),
    ],
)
def test_clean(formula_str, expected):
    assert clean(formula_str) == expected


@pytest.mark.parametrize(
    "formula,expected",
    [
        # ((A2B)3A)2
        ([2, ("A", 1), 3, ("B", 1), ("A", 2), "(", "("], {"A": 14, "B": 6}),
        # (C(A2B)3A)2
        (
            [2, ("A", 1), 3, ("B", 1), ("A", 2), "(", ("C", 1), "("],
            {"A": 14, "B": 6, "C": 2},
        ),
    ],
)
def test_multiply(formula, expected):
    assert multiply((e for e in formula)) == expected


def test_integration():
    pass
