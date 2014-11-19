import pytest

import jarg


def test_JSONDialect():
    dialect = jarg.JSONDialect()

    assert dialect.to_python("bar") == "bar"
    assert dialect.to_python("42") == 42
    assert dialect.to_python("4.20") == 4.2
    assert dialect.to_python('"69"') == "69"

    assert dialect.from_literal("true") == True
    assert dialect.from_literal("false") == False
    assert dialect.from_literal("[1, 2, 3]") == [1, 2, 3]
    assert dialect.from_literal("{\"bar\": \"baz\"}") == {'bar': 'baz'}


def test_FormDialect():
    dialect = jarg.FormDialect()

    assert dialect.to_python("foo") == "foo"

    assert dialect.from_literal("foo=bar") == {'foo': ['bar']}


def test_makepair():
    dialect = jarg.JSONDialect()

    assert jarg.makepair(dialect, "foo=bar") == ('foo', 'bar')
    assert jarg.makepair(dialect, "foo=42") == ('foo', 42)
    assert jarg.makepair(dialect, "foo:=\"123\"") == ('foo', '123')

    with pytest.raises(jarg.InvalidLiteralError):
        jarg.makepair(dialect, "foo:=[1")
