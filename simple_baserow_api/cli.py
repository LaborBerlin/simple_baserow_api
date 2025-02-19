"""CLI interface for simple_baserow_api project.
"""

import os
import sys
import json
from dataclasses import fields

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

        if args.fields_schema:
            with open(args.fields_schema) as f:
                fields = json.load(f)
        else:
            fields = None

        cls.api.get_jwt(cls.user, cls.passwd)
        cls.api.create_table(args.database_id, args.table_name, fields)


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
