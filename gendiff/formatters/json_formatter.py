import json


def format_diff(diff):
    return json.dumps(diff, indent=4, sort_keys=True)
