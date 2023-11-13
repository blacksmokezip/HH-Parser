import argparse
from parser.parse import parse_vacancies


def main():
    parser = argparse.ArgumentParser(
        description="Parses jobs from hh.ru"
    )

    parser.add_argument('query')

    parser.add_argument('-f', '--file',
                        dest='file',
                        help='set file to save vacancies',
                        default='vacancies.txt'
                        )

    args = parser.parse_args()

    try:
        parse_vacancies(args.query, args.file)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
