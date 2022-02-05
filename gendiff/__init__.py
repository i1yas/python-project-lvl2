import json

from gendiff.parsers import get_parser


def get_diff(old, new):
    old_keys = old.keys()
    new_keys = new.keys()
    all_keys = set(list(old_keys) + list(new_keys))
    all_keys_in_order = sorted(all_keys)

    diff = []

    for key in all_keys_in_order:
        old_value = old.get(key)
        new_value = new.get(key)

        if old_value == new_value:
            diff.append({
                'type': 'keep',
                'key': key,
                'value': old_value
            })
            continue

        if key in old_keys:
            diff.append({
                'type': 'remove',
                'key': key,
                'value': old_value
            })

        if key in new_keys:
            diff.append({
                'type': 'add',
                'key': key,
                'value': new_value
            })

    return diff


def format_value(value):
    if isinstance(value, str):
        return value
    return json.dumps(value)


def format_diff(diff):
    symbol_mapping = {
        'remove': '-',
        'add': '+',
        'keep': ' '
    }
    result = []
    tab = '  '

    for line in diff:
        type = line['type']
        symbol = symbol_mapping[type]
        key = line['key']
        value = line['value']
        result.append(f'{tab}{symbol} {key}: {format_value(value)}')

    return '\n'.join([
        '{',
        *result,
        '}'
    ])


def generate_diff(filepath1, filepath2):
    """
    Generates diff of two files
    """
    parse = get_parser(filepath1)
    old = parse(open(filepath1))
    new = parse(open(filepath2))
    diff = get_diff(old, new)

    return format_diff(diff)
