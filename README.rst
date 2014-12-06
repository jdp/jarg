====
jarg
====

.. image:: https://travis-ci.org/jdp/jarg.svg?branch=master
    :target: https://travis-ci.org/jdp/jarg

**jarg** is an encoding shorthand for your shell.
It is a command-line utility that makes generating data in formats like JSON, YAML, and form encoding easier in the shell.

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

The `name` portions have the same syntax and semantics as `HTML JSON`_ names::

    $ jarg foo[]=bar foo[]=baz bar[baz]=quux
    {"foo": ["bar", "baz"], "bar": {"baz": "quux"}}

You can also write literal values directly, using the `name:=value` syntax.
That lets you write things like booleans, lists, and explicit strings::

    $ jarg foo:=true bar:=\"123\"
    {"foo": true, "bar": "123"}
    $ jarg foo:=[1,2,3]
    {"foo": [1, 2, 3]}


Dialects
--------

The default dialect is JSON, and includes support for YAML and form encoding.

To use the YAML dialect, use the ``-y``/``--yaml`` switch::

    $ jarg -y name=jarg type="cli tool" traits[]=dope traits[]=rad
    ---
    name: jarg
    traits: [dope, rad]
    type: cli tool

You can switch to the form encoding dialect with the ``-f``/``--form`` switch::

    $ jarg -f foo=bar baz="jarg is dope"
    foo=bar&baz=jarg+is+dope

.. _PyPI: http://pypi.python.org/
.. _`HTML JSON`: http://www.w3.org/TR/html-json-forms/
