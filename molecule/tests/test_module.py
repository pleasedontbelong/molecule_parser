import pytest
from molecule.__main__ import run
from unittest.mock import patch


def test_run():
    with patch("molecule.__main__.parse", return_value={}) as parse_mock:
        run(*["foo", "H2O"])
        parse_mock.assert_called_once()


@pytest.mark.parametrize("arguments", ([], ["foo"], ["foo", "bar", "zee"]))
def test_run_invalid_arguments(arguments):
    with patch("molecule.__main__.parse"):
        with pytest.raises(SystemExit) as e:
            run(*arguments)
            assert e.type == SystemExit
            assert e.value.code == 1
