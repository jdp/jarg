====
jarg
====

**jarg** is a JSON shorthand for your shell. It is a command-line utility that wants to make writing JSON in the shell easier.

Installation
------------

Install from PyPI_::

    $ pip install jarg

Usage
-----

Each argument to **jarg** should be in the format of `name=value`.
Values are interpreted as their closest JSON value.
The most common case is probably string names and values::

    $ jarg foo=bar baz=quux
    {"foo": "bar", "baz": "quux"}

Floats and integers will work too::

    $ jarg foo=10 bar=4.2
    {"foo": 10, "bar": 4.2}

If you really need something to be a string,
you can surround the value in double quotes::

    $ jarg foo=\"123\"
    {"foo": "123"}

The value is optional.
If you leave it out, it is interpreted as ``null``::

    $ jarg foo
    {"foo": null}

You can also write JSON directly, using the `name:=value` syntax.
That lets you write things like booleans, lists, and nested objects::

    $ jarg foo:=true bar:=false
    {"foo": true, "bar": false}
    $ jarg foo:=[1,2,3]
    {"foo": [1, 2, 3]}

The literal JSON syntax also helps you nest objects::

    $ jarg foo:="$(jarg bar=baz quux=bux)"
    {"foo": {"quux": "bux", "bar": "baz"}}

.. _PyPI: http://pypi.python.org/
