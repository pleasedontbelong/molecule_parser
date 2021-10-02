import re

from molecule.validator import validate


def clean(formula):
    """
    Harmonize the formula. Replaces brackets and braces with parentheses, and
    adds a multiplier 1 at the end of every closing parentheses that doesn't have one

    :param str formula: String representation of a formula
    :return: Cleaned version of the formula
    :rtype: str
    """
    # remove spaces
    formula = re.sub(r"(\s+)", "", formula)
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
    """
    Returns a generator with each part (token) of the formula, reading it
    from rigth to left. We'll ignore closing parenthesis since the cleaning
    function will ensure a digit after every closing parenthesis. Chemical elements
    will be returned as a tuple including it's atoms count

    >>> list(tokenizer("(SK2Mg3)4"))
    [4, 3, ("Mg", 3), ("K", 2), ("S", 1)]

    :param str formula: (Cleaned) String representation of a formula
    :return: A generator including token for multipliers, elements
    :rtype: generator
    """
    formula = list(formula_str)
    while formula:
        token = formula.pop()
        if token == "(":
            yield token
        # if we find a lower case letter we'll pop the previous char too
        elif re.match(r"[a-z]", token):
            yield (f"{formula.pop()}{token}", 1)
        # if we find an upper case letter it will always be an element of one
        # single atom
        elif re.match(r"[A-Z]", token):
            yield (token, 1)
        # if we find a number we should check if it's preceded by a parenthesis
        # or an element
        elif token.isnumeric():
            digits = token
            # extract the whole number since there migth be multiple digits
            while formula[-1].isnumeric():
                digits = formula.pop() + digits
            digits = int(digits)

            previous = formula.pop()
            # if the previous character in the formula is a closing parentheses
            # we'll just ignore it and return the number instead
            if previous == ")":
                yield digits
            # if the previous char is a lower case letter then extract the whole
            # element symbol and return it as a tuple
            # (i.e `Mg3` digit=3, previous=g)
            elif re.match(r"[a-z]", previous):
                yield (f"{formula.pop()}{previous}", digits)
            # The only posibility left is an upper case letter, we'll return
            # the element with it's number of atoms as a tuple
            else:
                yield (previous, digits)


def multiply(formula, result_map=None, multiplier=1):
    """
    Recursive function that should apply the multipliers on the formula
    and recursively call the same function if a subformula is found

    :param generator formula: A tokenized version of the formula sent as a
                              generator (c.f. tokenizer)
    :param dict result_map: Default to none, used to recursively sent the subformula
    :param dict multiplier: Default to 1, used to apply the multiplier to the
                            subformula
    :return: A generator including token for multipliers, elements
    :rtype: generator
    """
    if result_map is None:
        result_map = {}

    # keep the multiplier on a different variable for the context of the recursive
    # calls
    current_multiplier = multiplier

    for token in formula:
        # on opening parentheses we've found the end of the subformula
        if token == "(":
            return result_map
        # when the token is an integer we've found a new subformula so we should
        # make the recursive call passing this token as multiplier
        if type(token) is int:
            current_multiplier = token
            sub_formula = multiply(formula, multiplier=current_multiplier)
            # after the multiplier was applied to the subfunction we should
            # update our result_map dict with the results
            for sub_element, value in sub_formula.items():
                result_map[sub_element] = (
                    result_map.get(sub_element, 0) + value * multiplier
                )
        # when the token is a tuple we've found an element so we should only
        # update the result_map applying the multiplier
        if type(token) is tuple:
            result_map[token[0]] = result_map.get(token[0], 0) + token[1] * multiplier
    return result_map


def parse_molecule(formula):
    """
    Cleans the formula, validates it and then calls the recursive function to
    do the hard work

    :param str formula: String representation of a formula
    """
    formula = clean(formula)
    validate(formula)
    return multiply(tokenizer(formula))
