import re

from molecule.models import Context


def clean(formula):
    """
    Harmonize the formula. Replaces brackets and braces with parentheses, and
    adds a number 1 at the end of every closing parentheses
    """
    # replaces start brackets
    formula = re.sub(r"[\[\{]", "(", formula)
    # replaces closing brackets
    formula = re.sub(r"[\]\}]", ")", formula)
    if not formula.startswith("("):
        formula = f"({formula})1"
    if re.match(r"^\(.*\)$", formula):
        formula = f"{formula}1"
    return re.sub(r"\)([A-Z\)\(\)])", r")1\1", formula)


def parse(formula):
    formula = clean(formula)
