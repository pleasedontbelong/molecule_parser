import sys
import json
from molecule.parser import parse


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
    return json.dumps(parse(args[1]))


if __name__ == "__main__":
    print(run(*sys.argv))
