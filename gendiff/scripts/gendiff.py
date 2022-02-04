import argparse


def main():
    parser = argparse.ArgumentParser(description="Generate diff")

    parser.add_argument('first_line', type=str)
    parser.add_argument('second_line', type=str)
    parser.add_argument('-f', '--format', dest='FORMAT', type=str,
                        help='set format of output')

    args = parser.parse_args()
    print(args.accumulate(args.integers))


if __name__ == '__main__':
    main()
