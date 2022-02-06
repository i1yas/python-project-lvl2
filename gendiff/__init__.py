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
        is_nested = isinstance(old_value, dict) and isinstance(new_value, dict)

        if is_nested:
            diff.append({
                'type': 'keep',
                'key': key,
                'chlidren': get_diff(old_value, new_value)
            })
            continue

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


symbol_mapping = {
    'remove': '-',
    'add': '+',
    'keep': ' '
}


def get_tab(symbol_type, depth):
    space = ' '
    symbol = symbol_mapping[symbol_type]
    tab = space * 4 * depth + space * 2 + symbol + space
    return tab


def format_key_value(key, value, symbol_type, depth):
    tab = get_tab(symbol_type, depth)
    return f'{tab}{key}: {value}'


def wrap_with_braces(content, depth):
    space = ' '
    return '\n'.join([
        '{',
        content,
        space * 4 * depth + '}'
    ])


def format_value(value, depth):
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        lines = map(
            lambda item: format_key_value(
                key=item[0],
                value=format_value(item[1], depth + 1),
                symbol_type='keep',
                depth=depth
            ),
            value.items())
        content = '\n'.join(list(lines))
        return wrap_with_braces(content, depth)

    return json.dumps(value)


def format_diff(diff):

    def walk(diff, depth):
        result = []

        for line in diff:
            type = line['type']
            key = line['key']
            value = line.get('value')
            chlidren = line.get('chlidren')

            formatted_value = ''
            if chlidren:
                formatted_value = walk(chlidren, depth + 1)
            else:
                formatted_value = format_value(
                    value,
                    depth=depth + 1
                )

            result.append(format_key_value(
                key=key,
                value=formatted_value,
                symbol_type=type,
                depth=depth
            ))

        content = '\n'.join(result)
        return wrap_with_braces(content, depth)

    return walk(diff, 0)


def generate_diff(filepath1, filepath2):
    """
    Generates diff of two files
    """
    parse = get_parser(filepath1)
    old = parse(open(filepath1))
    new = parse(open(filepath2))
    diff = get_diff(old, new)

    return format_diff(diff)
