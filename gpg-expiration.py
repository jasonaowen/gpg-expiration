#!/usr/bin/env python3

# Copyright (C) 2021 Jason Owen <jason@jasonaowen.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Check if a GPG key, or any of its subkeys, will expire soon.
"""

import argparse
from datetime import datetime, timedelta
import gpg
import sys


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'key_id',
        help='''GPG key ID to check.
        This can be any valid search string that uniquely identifies a key.''',
    )
    parser.add_argument(
        '--days',
        type=int,
        required=True,
        help='Check for key expiration within the next DAYS days',
    )
    return parser.parse_args()


def load_key(key_id):
    with gpg.Context() as ctx:
        try:
            return ctx.get_key(key_id, secret=False)
        except gpg.errors.GPGMEError as ex:
            raise ValueError('Unable to load key', key_id) from ex


def check_expiration(key_id, not_before):
    key = load_key(key_id)
    expiring_subkeys = [
        subkey for subkey in key.subkeys
        if subkey.expires != 0 and subkey.expires < not_before.timestamp()
    ]
    if expiring_subkeys:
        print(f'{key.uids[0].uid} will expire before {not_before}:')
        for subkey in expiring_subkeys:
            expires_at = datetime.fromtimestamp(subkey.expires)
            print(f'  {subkey.fpr} expires at {expires_at}')
        sys.exit(1)


if __name__ == "__main__":
    args = parse_args()
    not_before = datetime.today() + timedelta(days=args.days)
    check_expiration(
        args.key_id,
        not_before,
    )
