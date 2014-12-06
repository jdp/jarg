#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import sys

from . import __VERSION__
from .dialects import FormDialect, JSONDialect, YAMLDialect
from .jsonform import encode


class InvalidLiteralError(ValueError):
    def __init__(self, key, *args, **kwargs):
        self.key = key
        super(InvalidLiteralError, self).__init__(key, *args, **kwargs)


def makepair(dialect, pair):
    """Return a (key, value) tuple from a KEY=VALUE formatted string.
    """

    parts = pair.split('=', 1)
    if len(parts) == 1:
        parts.append(None)
    key, value = parts
    if key[-1] == ":":
        key = key[:-1]
        try:
            value = dialect.from_literal(value)
        except ValueError:
            raise InvalidLiteralError(key)
    else:
        value = dialect.to_python(value)
    return key, value


def fatal(msg, code=1):
    sys.stderr.write("{}: {}\n".format(os.path.basename(sys.argv[0]), msg))
    sys.exit(code)


def main():
    ap = argparse.ArgumentParser(
        description="Shorthand encoding format syntax.", prog="jarg")
    dialects = ap.add_mutually_exclusive_group()
    dialects.add_argument(
        '-j', '--json', action='store_const', const=JSONDialect,
        dest='dialect', help="use the JSON dialect")
    dialects.add_argument(
        '-y', '--yaml', action='store_const', const=YAMLDialect,
        dest='dialect', help="use the YAML dialect")
    dialects.add_argument(
        '-f', '--form', action='store_const', const=FormDialect,
        dest='dialect', help="use the form encoding dialect")
    ap.add_argument(
        'pair', nargs='+', help="a pair in the format of KEY=VALUE")
    ap.add_argument(
        '-V', '--version', action='version',
        version="%(prog)s {}".format('.'.join(__VERSION__)))
    args = ap.parse_args()

    dialect = (args.dialect or JSONDialect)()
    if sys.stdin.isatty():
        context = {}
    else:
        context = dialect.from_literal(sys.stdin.read())
    try:
        context.update(encode(makepair(dialect, pair) for pair in args.pair))
    except InvalidLiteralError as e:
        fatal("valid literal value required for key `{}'".format(e.key))
    sys.stdout.write(dialect.dumps(context))

if __name__ == '__main__':
    main()
