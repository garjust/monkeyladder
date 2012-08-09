#!/usr/bin/env python
import os
import sys

from monkeyladder.settings.development import DATABASES

FIXTURES = ['fixtures/users.json', 'fixtures/core.json', 'fixtures/leaderboard.json']

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    for database in DATABASES:
        database_file = DATABASES[database]['NAME']
        if not database_file.endswith('monkeyladder.db'):
            print "Bad File: {}".format(database_file)
            continue
        if not os.path.exists(database_file):
            print "Target database does not exist: {}".format(database_file)
            continue
        print "Killing database: {}".format(database_file)
        os.remove(database_file)

    execute_from_command_line([sys.argv[0], 'syncdb', '--noinput'])
    execute_from_command_line([sys.argv[0], 'loaddata'] + FIXTURES)

