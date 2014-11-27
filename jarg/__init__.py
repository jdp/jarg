#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json
import os
import sys
from urllib import urlencode
try:
    from urlparse import parse_qs
except ImportError:
    from urllib.parse import parse_qs

import jsonform


__VERSION__ = ('0', '3', '0')


class InvalidLiteralError(ValueError):
    def __init__(self, key, *args, **kwargs):
        self.key = key
        super(InvalidLiteralError, self).__init__(key, *args, **kwargs)


class BaseDialect(object):
    def from_literal(self, value):
        return value

    def to_python(self, value):
        return value

    def dumps(self, context):
        return str(context)


class JSONDialect(BaseDialect):
    def from_literal(self, value):
        return json.loads(value)

    def to_python(self, value):
        if value is None:
            return value
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass
        return value

    def dumps(self, context):
        return json.dumps(context, cls=jsonform.JSONFormEncoder)


class FormDialect(BaseDialect):
    def from_literal(self, value):
        return parse_qs(value)

    def to_python(self, value):
        if value is None:
            return ""
        return value

    def dumps(self, context):
        return urlencode(context)


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
        description="Shorthand encoding format syntax.")
    dialects = ap.add_mutually_exclusive_group()
    dialects.add_argument(
        '-j', '--json', action='store_const', const=JSONDialect,
        dest='dialect', help="use the JSON dialect")
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
    try:
        result = jsonform.encode(makepair(dialect, pair) for pair in args.pair)
    except InvalidLiteralError as e:
        fatal("valid literal value required for key `{}'".format(e.key))
    sys.stdout.write(dialect.dumps(result))

if __name__ == '__main__':
    main()
