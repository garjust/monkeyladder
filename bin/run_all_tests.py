#!/usr/bin/env python
import os
import sys

from django.core.management import execute_from_command_line

TESTABLE_APPS = ['accounts', 'ladders', 'leaderboard']


def run_app_tests(*apps_to_tests):
    execute_from_command_line(['manage.py', 'test', '--verbosity=2'] + list(apps_to_tests))

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))
    os.chdir(os.path.abspath(os.path.join(__file__, '..', '..')))

    run_app_tests(*TESTABLE_APPS)
