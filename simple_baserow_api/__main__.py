"""Entry point for simple_baserow_api."""
import argparse

from simple_baserow_api.cli import main  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    args = argparse.ArgumentParser('python -m simple_baserow_api')
    args.add_argument('--url')
    args.add_argument('--token')
    args.add_argument('--user')
    args.add_argument('--passwd')
    subargs = args.add_subparsers(dest='command', required=True)

    create_table_args = subargs.add_parser('create_table')
    create_table_args.add_argument('database_id', type=int)
    create_table_args.add_argument('table_name')
    create_table_args.add_argument('--fields_schema')

    main(args.parse_args())
