import re


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
    # Test (C(A2B)3A)2
    for e in [2, ("A", 1), 3, ("B", 1), ("A", 2), "(", ("C", 1), "("]:
        yield e
    # formula = list(formula_str)
    # while formula:
    #     token = formula.pop()
    #     if token in "()":
    #         yield token
    #     elif re.match(r"[A-Z]", token):
    #         next = formula[-1]
    #         element = token
    #         if re.match(r"[a-z]", next):
    #             element += formula.pop()
    #         if next.isnumeric():
    #             yield (element, formula.pop())
    #         else:
    #             yield (element, 1)
    #     elif token.isnumeric():
    #         yield int(token)


def multiply(result_map, formula, multiplier=1):
    current_multiplier = multiplier
    for element in formula:
        if element == "(":
            return result_map
        if type(element) is int:
            current_multiplier = element
            sub_formula = multiply({}, formula, multiplier=current_multiplier)
            for sub_element, value in sub_formula.items():
                result_map[sub_element] = (
                    result_map.get(sub_element, 0) + value * multiplier
                )

        if type(element) is tuple:
            result_map[element[0]] = element[1] * multiplier
    return result_map


def parse(formula):
    return multiply({}, tokenizer(clean(formula)))
