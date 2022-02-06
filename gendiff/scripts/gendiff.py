import argparse

from gendiff import generate_diff


def main():
    parser = argparse.ArgumentParser(description="Generate diff")

    parser.add_argument('first_line', type=str)
    parser.add_argument('second_line', type=str)
    parser.add_argument('-f', '--format', dest='FORMAT', type=str,
                        help='set format of output')

    args = parser.parse_args()
    diff = generate_diff(
        args.first_line,
        args.second_line,
        type=args.FORMAT or 'json'
    )
    print(diff)


if __name__ == '__main__':
    main()
