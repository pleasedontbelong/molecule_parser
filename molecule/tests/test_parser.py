import pytest
from molecule.parser import clean


@pytest.mark.parametrize(
    "formula,expected",
    [
        ("A", "(A)1"),
        ("(A)", "(A)1"),
        ("(AB)2", "(AB)2"),
        ("(AB1)23", "(AB1)23"),
        ("A[B]", "(A(B)1)1"),
        ("{A[B]}2", "(A(B)1)2"),
        ("(A(B))", "(A(B)1)1"),
        ("ABC(DE)(FG)", "(ABC(DE)1(FG)1)1"),
    ],
)
def test_clean(formula, expected):
    assert clean(formula) == expected
