from molecule.parser import parse


def test_parser():
    assert parse("H2O") == {"H": 2, "O": 1}
