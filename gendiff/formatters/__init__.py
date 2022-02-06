from gendiff.formatters import (
    plain_formatter,
    json_formatter,
    stylish_formatter
)


mapping = {
    'stylish': stylish_formatter.format_diff,
    'plain': plain_formatter.format_diff,
    'json': json_formatter.format_diff
}


def get_formatter(name):
    format = mapping.get(name.lower())
    if not format:
        raise Exception(f'Unknown formatter "{name}"')
    return mapping[name.lower()]
