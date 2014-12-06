import pytest

from jarg.cli import InvalidLiteralError, makepair
from jarg.dialects import JSONDialect


def test_makepair():
    dialect = JSONDialect()

    assert makepair(dialect, "foo=bar") == ('foo', 'bar')
    assert makepair(dialect, "foo=42") == ('foo', 42)
    assert makepair(dialect, "foo:=\"123\"") == ('foo', '123')

    with pytest.raises(InvalidLiteralError):
        makepair(dialect, "foo:=[1")
