# -*- coding: utf-8 -*-
import json
try:
    from urllib import urlencode
    from urlparse import parse_qs
except ImportError:
    from urllib.parse import parse_qs, urlencode

import yaml

from .jsonform import JSONFormEncoder


class BaseDialect(object):
    def from_literal(self, value):
        return value

    def to_python(self, value):
        return value

    def dumps(self, context):
        return str(context)


class CoerceMixin(object):
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


class JSONDialect(CoerceMixin, BaseDialect):
    def from_literal(self, value):
        return json.loads(value)

    def dumps(self, context):
        return json.dumps(context, cls=jsonform.JSONFormEncoder)


class YAMLDialect(CoerceMixin, BaseDialect):
    def from_literal(self, value):
        return yaml.load(value)


class FormDialect(BaseDialect):
    def from_literal(self, value):
        return parse_qs(value)

    def to_python(self, value):
        if value is None:
            return ""
        return value

    def dumps(self, context):
        return urlencode(context)
