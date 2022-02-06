import json


def format_value(value):
    if isinstance(value, dict):
        return '[complex value]'
    if isinstance(value, str):
        return f'\'{value}\''
    return json.dumps(value)


def format_line(path, line):
    type = line['type']
    path_str = '.'.join(path)

    if type == 'update':
        old = format_value(line['old'])
        new = format_value(line['new'])
        return f'Property \'{path_str}\' was updated. From {old} to {new}'

    if type == 'remove':
        return f'Property \'{path_str}\' was removed'

    if type == 'add':
        value = format_value(line['value'])
        return f'Property \'{path_str}\' was added with value: {value}'


def format_diff(diff):
    def walk(lines, path):
        result = []
        for line in lines:
            key = line['key']
            children = line.get('children')
            new_path = path + [key]

            if children:
                result.extend(walk(children, new_path))
                continue

            formatted_line = format_line(new_path, line)
            if formatted_line:
                result.append(formatted_line)

        return result

    formatted_lines = walk(diff, [])
    return '\n' + '\n'.join(formatted_lines)
