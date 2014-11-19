import pytest

import jarg


def test_makepair():
    assert jarg.makepair("foo=bar") == ('foo', 'bar')
    assert jarg.makepair("foo=42") == ('foo', 42)
    assert jarg.makepair("foo=4.20") == ('foo', 4.2)
    assert jarg.makepair('foo="69"') == ('foo', '69')
    assert jarg.makepair("foo") == ('foo', None)

    assert jarg.makepair("foo:=true") == ('foo', True)
    assert jarg.makepair("foo:=false") == ('foo', False)
    assert jarg.makepair("foo:=[1, 2, 3]") == ('foo', [1, 2, 3])
    assert jarg.makepair("foo:={\"bar\": \"baz\"}") == ('foo', {'bar': 'baz'})

    with pytest.raises(jarg.InvalidJSONError):
        jarg.makepair("foo:=[1,")
