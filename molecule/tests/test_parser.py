import pytest
from molecule.parser import clean, multiply, parse, tokenizer


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
    "formula_str,expected",
    [
        ("(A)1", [1, ("A", 1), "("]),
        ("(A12B)345", [345, ("B", 1), ("A", 12), "("]),
        ("(AbC)1", [1, ("C", 1), ("Ab", 1), "("]),
        ("(Ab2C)3", [3, ("C", 1), ("Ab", 2), "("]),
        ("(Ab23C)4", [4, ("C", 1), ("Ab", 23), "("]),
        ("((A2)3(B)4)5", [5, 4, ("B", 1), "(", 3, ("A", 2), "(", "("]),
    ],
)
def test_tokenizer(formula_str, expected):
    assert list(tokenizer(formula_str)) == expected


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
        # ((A2)3(B)4)5
        ([5, 4, ("B", 1), "(", 3, ("A", 2), "(", "("], {"A": 30, "B": 20}),
    ],
)
def test_multiply(formula, expected):
    assert multiply((e for e in formula)) == expected
