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
    create_table_args.add_argument('--create_fields', action='store_true',
                                   help='Also create fields. Fields schema JSON data as obtained from get_fields is '
                                        'read from stdin.')
    create_table_args.add_argument('--fail_on_error', action='store_true',
                                   help='Fail if error appears.')

    add_data_args = subargs.add_parser('add_data',
                                       help='Add/Change data for a table. Rows are read from stdin as JSON data like '
                                            'obtained from get_data')
    add_data_args.add_argument('table_id', type=int)
    add_data_args.add_argument('--field_ids', action='store_true',
                               help='Use field IDs instead of user field names.')
    add_data_args.add_argument('--force_insert', action='store_true',
                               help="Always insert and don't update entries.")
    add_data_args.add_argument('--limit', type=int,
                               help="Add only the first n rows.")
    add_data_args.add_argument('--fail_on_error', action='store_true',
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
                               help='Return field IDs instead of user field names.')
    get_data_args.add_argument('--json_indent', type=int)

    json_to_csv_args = subargs.add_parser('json_to_csv',
                                          help="Transform JSON data as retrieved via get_data and read via stdin to "
                                               "CSV printed to stderr.")

    main(args.parse_args())
