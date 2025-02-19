"""CLI interface for simple_baserow_api project.
"""

import os
import sys
import json

from simple_baserow_api import BaserowApi


def fail_if_missing_arg(argname, argv):
    if argv is None:
        print(f'Required baserow API {argname} not given.', file=sys.stderr)
        sys.exit(1)


class Commands:
    api = None    # type: BaserowApi
    user = None
    passwd = None

    @classmethod
    def create_table(cls, args):
        fail_if_missing_arg('user', cls.user)
        fail_if_missing_arg('password', cls.passwd)

        if args.create_fields:
            fields = json.load(sys.stdin)
        else:
            fields = None

        cls.api.get_jwt(cls.user, cls.passwd)
        tab_id = cls.api.create_table(args.database_id, args.table_name, fields)
        print(f'created table with ID {tab_id}')

    @classmethod
    def add_data(cls, args):
        data = json.load(sys.stdin)

        if isinstance(data, dict) and 'results' in data.keys():
            data = data['results']
        else:
            data = list(data.values())

        cls.api.add_data_batch(args.table_id, data,
                               user_field_names=not args.field_ids,
                               fail_on_error=args.fail_on_error)

    @classmethod
    def get_fields(cls, args):
        fields = cls.api.get_fields(args.table_id)
        print(json.dumps(fields, indent=args.json_indent))

    @classmethod
    def get_data(cls, args):
        rows = cls.api.get_data(args.table_id,
                                writable_only=not args.include_non_writable_fields,
                                user_field_names=not args.field_ids)
        print(json.dumps(rows, indent=args.json_indent))


def main(args):
    cmd = args.command

    baseurl = args.url or os.environ.get('BASEROWAPI_URL', None)
    fail_if_missing_arg('URL', baseurl)

    token = args.url or os.environ.get('BASEROWAPI_TOKEN', None)
    fail_if_missing_arg('Token', token)

    Commands.user = args.user or os.environ.get('BASEROWAPI_USER', None)
    Commands.passwd = args.passwd or os.environ.get('BASEROWAPI_PASSWD', None)
    Commands.api = BaserowApi(baseurl, token)

    method = getattr(Commands, cmd)
    method(args)
