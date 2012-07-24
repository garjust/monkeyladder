#!/usr/bin/env python
import os
import sys

from monkeyladder.settings.development import DATABASES

def kill():
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

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monkeyladder.settings.production")

    from django.core.management import execute_from_command_line

    fixtures = ['fixtures/users.json', 'fixtures/core.json', 'fixtures/leaderboard.json']
    if len(sys.argv) > 1:
        if sys.argv[1] == "newdb":
            kill()
            execute_from_command_line([sys.argv[0], 'syncdb', '--noinput'])
            execute_from_command_line([sys.argv[0], 'loaddata'] + fixtures)
            exit(0)

    execute_from_command_line(sys.argv)

