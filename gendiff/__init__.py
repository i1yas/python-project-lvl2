import json


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
        result.append(f'{tab}{symbol} {line["key"]}: {line["value"]}')

    return '\n'.join([
        '{',
        *result,
        '}'
    ])


def generate_diff(filepath1, filepath2):
    """
    Generates diff of two files
    """
    old = json.load(open(filepath1))
    new = json.load(open(filepath2))
    diff = get_diff(old, new)

    return format_diff(diff)
