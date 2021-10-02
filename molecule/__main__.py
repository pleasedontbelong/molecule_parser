import sys
import json
from molecule.exceptions import InvalidFormula
from molecule.parser import parse_molecule


def run(*args):
    if len(args) != 2:
        print(
            """
Error! Formula should be passed as argument to the modue.
e.g.
python -m molecule "H2O"
"""
        )
        exit(1)
    try:
        return json.dumps(parse_molecule(args[1]))
    except InvalidFormula as e:
        print(str(e))
        exit(1)


if __name__ == "__main__":
    print(run(*sys.argv))
