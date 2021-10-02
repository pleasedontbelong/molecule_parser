import re
from molecule.constants import KNOWN_ELEMENTS
from molecule.exceptions import (
    InvalidFormulaParentheses,
    InvalidFormulaElements,
    InvalidFormulaFormat,
)


def validate(formula_str):
    """
    Validates the format of the formula.

    Raises an InvalidFormula exception.
    """

    # Validate element symbol format (Uppercase char that migth be followed by a
    # lowercase char)
    check_element_format = re.sub("([A-Z][a-z]?)", "", formula_str)
    check_element_format = re.sub("([()0-9]?)", "", check_element_format)
    if len(check_element_format) > 0:
        raise InvalidFormulaFormat(
            f"Invalid Formula. Unexpected characters found: {check_element_format}"
        )

    # Validate opening and closing parentheses
    if formula_str.count("(") != formula_str.count(")"):
        raise InvalidFormulaParentheses(
            "Invalid Formula. Oppening and closing parentheses do not match"
        )

    # Validate element exists
    unknown_elements = [
        element.group(0)
        for element in re.finditer("([A-Z][a-z]?)", formula_str)
        if element.group(0) not in KNOWN_ELEMENTS
    ]

    if unknown_elements:
        raise InvalidFormulaElements(
            f"Invalid Formula. Unknown elements found: {', '.join(unknown_elements)}"
        )

    return True
