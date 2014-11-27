import pytest

from jarg.jsonform import encode, undefined


def test_encode():
    pairs = [('bottle-on-wall', 1), ('bottle-on-wall', 2), ('bottle-on-wall', 3)]
    output = {'bottle-on-wall': [1, 2, 3]}
    assert encode(pairs) == output

    pairs = [('pet[species]', 'Dahut'), ('pet[name]', 'Hypatia'), ('kids[1]', 'Thelma'), ('kids[0]', 'Ashley')]
    output = {"pet": {"species": "Dahut", "name": "Hypatia"}, "kids": ["Ashley", "Thelma"]}
    assert encode(pairs) == output

    pairs = [('pet[0][species]', 'Dahut'), ('pet[0][name]', 'Hypatia'), ('pet[1][species]', "Felis Stultus"), ('pet[1][name]', 'Billie')]
    output = {"pet": [{"species": "Dahut", "name": "Hypatia"}, {"species": "Felis Stultus", "name": "Billie"}]}
    assert encode(pairs) == output

    pairs = [("wow[such][deep][3][much][power][!]", "Amaze")]
    output = {'wow': {'such': {'deep': [undefined, undefined, undefined, {'much': {'power': {'!': 'Amaze'}}}]}}}
    assert encode(pairs) == output

    pairs = [('mix', 'scalar'), ('mix[0]', "array 1"), ('mix[2]', "array 2"), ('mix[key]', "key key"), ('mix[car]', "car key")]
    output = {"mix": {"": "scalar", 0: "array 1", 2: "array 2", "key": "key key", "car": "car key"}}
    assert encode(pairs) == output

    pairs = [('highlander[]', 'one')]
    output = {'highlander': ['one']}
    assert encode(pairs) == output

    pairs = [('error[good]', 'BOOM!'), ('error[bad', 'BOOM BOOM!')]
    output = {'error': {'good': 'BOOM!'}, 'error[bad': 'BOOM BOOM!'}
    assert encode(pairs) == output
