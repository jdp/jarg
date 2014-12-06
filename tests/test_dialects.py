import pytest

from jarg.dialects import FormDialect, JSONDialect


def test_JSONDialect():
    dialect = JSONDialect()

    assert dialect.to_python("bar") == "bar"
    assert dialect.to_python("42") == 42
    assert dialect.to_python("4.20") == 4.2
    assert dialect.to_python('"69"') == '"69"'

    assert dialect.from_literal("true") == True
    assert dialect.from_literal("false") == False
    assert dialect.from_literal("[1, 2, 3]") == [1, 2, 3]
    assert dialect.from_literal("{\"bar\": \"baz\"}") == {'bar': 'baz'}


def test_FormDialect():
    dialect = FormDialect()

    assert dialect.to_python("foo") == "foo"

    assert dialect.from_literal("foo=bar") == {'foo': ['bar']}

