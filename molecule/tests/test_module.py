import pytest
from molecule.__main__ import run
from unittest.mock import patch

from molecule.exceptions import InvalidFormula


def test_run():
    """
    Should run normally
    """
    with patch("molecule.__main__.parse_molecule", return_value={}) as parse_mock:
        run("foo", "H2O")
        parse_mock.assert_called_once()


@pytest.mark.parametrize("arguments", ([], ["foo"], ["foo", "bar", "zee"]))
def test_run_invalid_arguments(arguments):
    """
    Should raise a SystemExit (exit code 1) when too many arguments or too few
    arguments were sent to the module
    """
    with patch("molecule.__main__.parse_molecule"):
        with pytest.raises(SystemExit) as e:
            run(*arguments)
            assert e.type == SystemExit
            assert e.value.code == 1


def test_exception():
    """
    Should raise a SystemExit (exit code 1) when there's an error validating
    the formula
    """
    with patch("molecule.__main__.parse_molecule") as parse_mock:
        parse_mock.side_effect = InvalidFormula("Boom!")
        with pytest.raises(SystemExit) as e:
            run("foo", "quack")
            assert e.type == SystemExit
            assert e.value.code == 1
        parse_mock.assert_called_once()
