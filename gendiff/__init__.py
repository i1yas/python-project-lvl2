from gendiff.parsers import get_parser
from gendiff.formatters import get_formatter


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
                'children': get_diff(old_value, new_value)
            })
            continue

        if old_value == new_value:
            diff.append({
                'type': 'keep',
                'key': key,
                'value': old_value
            })
            continue

        if key in old_keys and key in new_keys:
            diff.append({
                'type': 'update',
                'key': key,
                'old': old_value,
                'new': new_value
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


def generate_diff(filepath1, filepath2, type='json'):
    """
    Generates diff of two files
    """
    parse = get_parser(filepath1)
    old = parse(open(filepath1))
    new = parse(open(filepath2))
    diff = get_diff(old, new)
    format = get_formatter(type)

    return format(diff)
