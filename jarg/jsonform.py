# -*- coding: utf-8 -*-
import json

undefined = object()


class JSONFormEncoder(json.JSONEncoder):
    def default(self, obj):
        if obj == undefined:
            return None
        else:
            return super(JSONFormEncoder, self).default(obj)


def parse_path(path):
    """
    http://www.w3.org/TR/2014/WD-html-json-forms-20140529/#dfn-steps-to-parse-a-json-encoding-path
    """
    original = path
    failure = [(original, {'last': True, 'type': object})]
    steps = []
    try:
        first_key = path[:path.index("[")]
        if not first_key:
            return original
        steps.append((first_key, {'type': 'object'}))
        path = path[path.index("["):]
    except ValueError:
        return failure
    while path:
        if path.startswith("[]"):
            steps[-1][1]['append'] = True
            path = path[2:]
            if path:
                return failure
        elif path[0] == "[":
            path = path[1:]
            try:
                key = path[:path.index("]")]
                path = path[path.index("]")+1:]
            except ValueError:
                return failure
            try:
                steps.append((int(key), {'type': 'array'}))
            except ValueError:
                steps.append((key, {'type': 'object'}))
        else:
            return failure
    for i in range(len(steps)-1):
        steps[i][1]['type'] = steps[i+1][1]['type']
    steps[-1][1]['last'] = True
    return steps


def set_value(context, step, current_value, entry_value):
    """
    http://www.w3.org/TR/2014/WD-html-json-forms-20140529/#dfn-steps-to-set-a-json-encoding-value
    """
    key, flags = step
    if flags.get('last', False):
        if current_value == undefined:
            if flags.get('append', False):
                context[key] = [entry_value]
            else:
                if isinstance(context, list) and len(context) <= key:
                    context.extend([undefined] * (key - len(context) + 1))
                context[key] = entry_value
        elif isinstance(current_value, list):
            context[key].append(entry_value)
        elif isinstance(current_value, dict):
            set_value(
                current_value, ("", {'last': True}),
                current_value.get("", undefined), entry_value)
        else:
            context[key] = [current_value, entry_value]
        return context
    else:
        if current_value == undefined:
            if flags.get('type') == 'array':
                context[key] = []
            else:
                if isinstance(context, list) and len(context) <= key:
                    context.extend([undefined] * (key - len(context) + 1))
                context[key] = {}
            return context[key]
        elif isinstance(current_value, dict):
            return context[key]
        elif isinstance(current_value, list):
            if flags.get('type') == 'array':
                return current_value
            else:
                obj = {}
                for i, item in enumerate(current_value):
                    if item != undefined:
                        obj[i] = item
                else:
                    context[key] = obj
                return obj
        else:
            obj = {"": current_value}
            context[key] = obj
            return obj


def encode(pairs):
    """
    The application/json form encoding algorithm.
    http://www.w3.org/TR/2014/WD-html-json-forms-20140529/#the-application-json-encoding-algorithm
    """
    result = {}
    for key, value in pairs:
        steps = parse_path(key)
        context = result
        for step in steps:
            try:
                current_value = context.get(step[0], undefined)
            except AttributeError:
                try:
                    current_value = context[step[0]]
                except IndexError:
                    current_value = undefined
            context = set_value(context, step, current_value, value)
    return result
