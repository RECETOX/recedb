from argparse import ArgumentParser

from metabodb.fetch import fetch

options = ArgumentParser(prog='metabodb')
commands = options.add_subparsers(title='commands')

fetch_options = commands.add_parser('fetch', help='fetch compounds from database exports')
fetch_options.add_argument('src', nargs='+', help='')
fetch_options.add_argument('dst', help='')
fetch_options.set_defaults(func=fetch)

args = options.parse_args()
args.func(args)
