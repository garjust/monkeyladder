#!/usr/bin/env python
import os
import sys

FIXTURES = ['fixtures/users.json', 'fixtures/ladders.json', 'fixtures/leaderboard.json']


def destroy_databases(databases):
    for database in databases:
        database_file = DATABASES[database]['NAME']
        if not database_file.endswith('.db'):
            print "Bad File: {}".format(database_file)
            continue
        if not os.path.exists(database_file):
            print "Target database does not exist: {}".format(database_file)
            continue
        print "Killing database: {}".format(database_file)
        os.remove(database_file)


def sync_new_database(fixtures):
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'syncdb', '--noinput'])
    execute_from_command_line(['manage.py', 'loaddata'] + fixtures)

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))
    os.chdir(os.path.abspath(os.path.join(__file__, '..', '..', 'project')))

    from project.monkeyladder.settings.development import DATABASES
    destroy_databases(DATABASES)

    sync_new_database(FIXTURES)
