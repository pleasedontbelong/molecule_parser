# molecule_parser

** Works on Python ~3.9.5 **

For a given chemical formula represented by a string, it counts the number of atoms of each element contained in the molecule and returns a dict with that information.

e.g. `K4[ON(SO3)2]2` returns `return {'K': 4, 'O': 14, 'N': 2, 'S': 4}`
It accepts parentheses, brackets and curly brackets as grouping chars

**Note: ** currently it does not validate the input ;) (missing closing parenthesis, non-existing element, etc.) I'm assuming you'll give me something that makes sense

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
$ pytest .
```
