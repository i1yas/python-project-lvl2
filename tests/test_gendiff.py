import os
import pytest

from gendiff import generate_diff


@pytest.fixture
def get_fixture_path():
    test_dir = os.path.dirname(os.path.realpath(__file__))

    def inner(name):
        return os.path.join(test_dir, 'fixtures', name)

    return inner


def test_gendiff(get_fixture_path):
    with open(get_fixture_path('expected.txt')) as f:
        expected = f.read()
        filepath1 = get_fixture_path('file1.json')
        filepath2 = get_fixture_path('file2.json')

        assert generate_diff(filepath1, filepath2) == expected


def test_gendiff_yaml(get_fixture_path):
    with open(get_fixture_path('expected.txt')) as f:
        expected = f.read()
        filepath1 = get_fixture_path('file1.yml')
        filepath2 = get_fixture_path('file2.yml')

        assert generate_diff(filepath1, filepath2) == expected
