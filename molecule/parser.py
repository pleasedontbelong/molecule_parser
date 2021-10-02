import re

from molecule.validator import validate


def clean(formula):
    """
    Harmonize the formula. Replaces brackets and braces with parentheses, and
    adds a multiplier 1 at the end of every closing parentheses that doesn't have one
    """
    # replaces start brackets
    formula = re.sub(r"[\[\{]", "(", formula)
    # replaces closing brackets
    formula = re.sub(r"[\]\}]", ")", formula)
    # ensure wrapping parentheses around formula
    if not formula.startswith("("):
        formula = f"({formula})1"
    # ensure multiplier at the end of the formula
    if re.match(r"^\(.*\)$", formula):
        formula = f"{formula}1"
    # ensure multiplier after a closing parentheses
    return re.sub(r"\)([A-Z\)\(\)])", r")1\1", formula)


def tokenizer(formula_str):
    formula = list(formula_str)
    while formula:
        token = formula.pop()
        if token == "(":
            yield token
        elif re.match(r"[a-z]", token):
            yield (f"{formula.pop()}{token}", 1)
        elif re.match(r"[A-Z]", token):
            yield (token, 1)
        elif token.isnumeric():
            digits = token
            while formula[-1].isnumeric():
                digits = formula.pop() + digits
            digits = int(digits)
            previous = formula.pop()
            if previous == ")":
                yield digits
            elif re.match(r"[a-z]", previous):
                yield (f"{formula.pop()}{previous}", digits)
            else:
                yield (previous, digits)


def multiply(formula, result_map=None, multiplier=1):
    if result_map is None:
        result_map = {}
    current_multiplier = multiplier
    for element in formula:
        if element == "(":
            return result_map
        if type(element) is int:
            current_multiplier = element
            sub_formula = multiply(formula, multiplier=current_multiplier)
            for sub_element, value in sub_formula.items():
                result_map[sub_element] = (
                    result_map.get(sub_element, 0) + value * multiplier
                )

        if type(element) is tuple:
            result_map[element[0]] = (
                result_map.get(element[0], 0) + element[1] * multiplier
            )
    return result_map


def parse_molecule(formula):
    formula = clean(formula)
    validate(formula)
    return multiply(tokenizer(formula))
