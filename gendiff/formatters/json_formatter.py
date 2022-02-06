import json


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
            children = line.get('children')

            if type == 'update':
                old = line['old']
                new = line['new']
                result.extend([
                    format_key_value(
                        key=key,
                        value=format_value(old, depth + 1),
                        symbol_type='remove',
                        depth=depth
                    ),
                    format_key_value(
                        key=key,
                        value=format_value(new, depth + 1),
                        symbol_type='add',
                        depth=depth
                    )
                ])
                continue

            formatted_value = ''
            if children:
                formatted_value = walk(children, depth + 1)
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
