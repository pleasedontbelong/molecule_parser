import pytest
from molecule.exceptions import (
    InvalidFormulaElements,
    InvalidFormulaFormat,
    InvalidFormulaParentheses,
)
from molecule.validator import validate


@pytest.mark.parametrize(
    "formula_str",
    ["K", "KMg", "BBe" "K(S2)O3Mg"],
)
def test_valid_formula(formula_str):
    """
    Should validate format, existence of elements and expected characters
    """
    assert validate(formula_str)


@pytest.mark.parametrize(
    "formula_str,exception",
    [
        ("a", InvalidFormulaFormat),
        ("Abc", InvalidFormulaFormat),
        ("ABcd", InvalidFormulaFormat),
        ("(ABc)d", InvalidFormulaFormat),
        ("(ABc)dE", InvalidFormulaFormat),
        ("(ABc)d2E", InvalidFormulaFormat),
        ("(K-/Mg?)2", InvalidFormulaFormat),
        ("(K)Mg)", InvalidFormulaParentheses),
        ("K)Mg)", InvalidFormulaParentheses),
        ("KMg))", InvalidFormulaParentheses),
        ("Z", InvalidFormulaElements),
        ("K2Xx2Y", InvalidFormulaElements),
    ],
)
def test_invalid_formula(formula_str, exception):
    """
    Should raise an exception in case of invalid format, unbalanced parentheses
    or unknown elements
    """
    with pytest.raises(exception) as e:
        validate(formula_str)
        assert e.type == exception
        assert e.value.code == 1
