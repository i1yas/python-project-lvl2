from gendiff.parsers import get_parser
from gendiff.formatters import get_formatter


def get_diff_item(key, keys, values):
    old_keys, new_keys = keys
    old_value, new_value = values
    is_nested = isinstance(old_value, dict) and isinstance(new_value, dict)

    if is_nested:
        return {
            'type': 'keep',
            'key': key,
            'children': get_diff(old_value, new_value)
        }

    if old_value == new_value:
        return {
            'type': 'keep',
            'key': key,
            'value': old_value
        }

    if key in old_keys and key in new_keys:
        return {
            'type': 'update',
            'key': key,
            'old': old_value,
            'new': new_value
        }

    if key in old_keys:
        return {
            'type': 'remove',
            'key': key,
            'value': old_value
        }

    if key in new_keys:
        return {
            'type': 'add',
            'key': key,
            'value': new_value
        }


def get_diff(old, new):
    old_keys = old.keys()
    new_keys = new.keys()
    all_keys = set(list(old_keys) + list(new_keys))
    all_keys_in_order = sorted(all_keys)

    diff = []

    for key in all_keys_in_order:
        keys = (
            old_keys,
            new_keys
        )
        values = (
            old.get(key),
            new.get(key)
        )

        diff.append(get_diff_item(
            key,
            keys,
            values
        ))

    return diff


def generate_diff(filepath1, filepath2, type=None):
    """
    Generates diff of two files
    """
    parse = get_parser(filepath1)
    old = parse(open(filepath1))
    new = parse(open(filepath2))
    diff = get_diff(old, new)
    format = get_formatter(type or 'stylish')

    return format(diff)
