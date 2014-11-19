====
jarg
====

**jarg** is an encoding shorthand for your shell.
It is a command-line utility that wants to make writing things like JSON and form-encoded values easier in the shell.

Installation
------------

Install from PyPI_::

    $ pip install jarg

Usage
-----

Each argument to **jarg** should be in the format of `name=value`.
Values are interpreted as their closest native encoding value, and the default dialect is JSON.
The most common case is probably string names and values::

    $ jarg foo=bar baz=quux
    {"foo": "bar", "baz": "quux"}

Floats and integers will work too::

    $ jarg foo=10 bar=4.2
    {"foo": 10, "bar": 4.2}

The value is optional.
If you leave it out, it is interpreted as ``null``::

    $ jarg foo
    {"foo": null}

You can also write literal values directly, using the `name:=value` syntax.
That lets you write things like booleans, lists, and explicit strings::

    $ jarg foo:=true bar:=\"123\"
    {"foo": true, "bar": "123"}
    $ jarg foo:=[1,2,3]
    {"foo": [1, 2, 3]}

The literal syntax also lets you nest values in recursive dialects::

    $ jarg foo:="$(jarg bar=baz quux=bux)"
    {"foo": {"quux": "bux", "bar": "baz"}}


Dialects
--------

The default dialect is JSON.
You can switch to the form encoding dialect with the ``-f`` switch::

    $ jarg -f foo=bar baz="jarg is dope"
    foo=bar&baz=jarg+is+dope

.. _PyPI: http://pypi.python.org/
