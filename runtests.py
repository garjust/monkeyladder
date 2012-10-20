#!/usr/bin/env python
import sys

from django.core.management import execute_from_command_line


def run():
    execute_from_command_line([sys.argv[0], 'test', '--verbosity=2', 'accounts'])
    execute_from_command_line([sys.argv[0], 'test', '--verbosity=2', 'core'])
    execute_from_command_line([sys.argv[0], 'test', '--verbosity=2', 'leaderboard'])

if __name__ == "__main__":
    run()
