import os
import json
import yaml


def parse_yaml(fd):
    return yaml.load(fd, Loader=yaml.Loader)


def get_parser(filepath):
    _, ext = os.path.splitext(filepath)

    mapping = {
        '.json': json.load,
        '.yaml': parse_yaml,
        '.yml': parse_yaml
    }

    return mapping[ext]
