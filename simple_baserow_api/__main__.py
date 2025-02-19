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
    create_table_args.add_argument('fields_schema', nargs='?',
                                   help='Path to JSON file with fields schema as obtained from get_fields.')

    insert_rows_args = subargs.add_parser('add_data')
    insert_rows_args.add_argument('table_id', type=int)
    insert_rows_args.add_argument('data', help='Path to JSON file with data rows as from get_data.')
    insert_rows_args.add_argument('--field_ids', action='store_true',
                                  help='Return user field IDs instead of field names.')
    insert_rows_args.add_argument('--fail_on_error', action='store_true',
                                  help='Fail if error appears.')

    get_fields_args = subargs.add_parser('get_fields')
    get_fields_args.add_argument('table_id', type=int)
    get_fields_args.add_argument('--json_indent', type=int)

    get_data_args = subargs.add_parser('get_data')
    get_data_args.add_argument('table_id', type=int)
    get_data_args.add_argument('--include_non_writable_fields', action='store_true',
                               help='Also return fields which cannot be written to. This includes all formula and '
                                    'computed fields.')
    get_data_args.add_argument('--field_ids', action='store_true',
                               help='Return user field IDs instead of field names.')
    get_data_args.add_argument('--json_indent', type=int)

    main(args.parse_args())
