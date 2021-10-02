# molecule_parser

**Currently tested on Python 3.8, 3.9**

[![pleasedontbelong](https://circleci.com/gh/pleasedontbelong/molecule_parser.svg?style=svg)](https://circleci.com/gh/pleasedontbelong/molecule_parser)

For a given chemical formula represented by a string, it counts the number of atoms of each element contained in the molecule and returns a dict with that information.

e.g. `K4[ON(SO3)2]2` returns `return {'K': 4, 'O': 14, 'N': 2, 'S': 4}`
It accepts parentheses, brackets and curly brackets as grouping chars, but the will all be considered as equals, i.e. `(K[S3]2{H}4)5` will be treated as `(K(S3)2(H)4)5`. Spaces will be ignored inside the formula.

The `parse_molecule` raise an `InvalidFormula` exception if a problem was found on the formula's format. We check the existence of the element and the balance of parentheses.

# Installing

```
pip install git+https://github.com/pleasedontbelong/molecule_parser.git#egg=molecule
```

# Usage

- Inside python:

```sh
from molecule import parse_molecule
parse_molecule("H2O")
```

- As a module, it will print a JSON representation of the atoms on the molecule

```sh
python -m molecule "H2O"
```

# Development

## Install on development mode

In order to launch the tests, you must install the packages inside `requirements.dev.txt`.

Inside a virtualenv call:

```sh
pip install -r requirements.dev.txt
```

## Tests

Tests were made with pytest using coverage.

```sh
pytest .
```

You can also launch the tests on different python versions:

```sh
tox
```

## Lint

Currently using `flake8` for checking pep8 and autoformatting using `black`.

```sh
flake8 .
black . --check
```
