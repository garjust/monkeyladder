#!/usr/bin/env python
import os
import sys

from django.core.management import execute_from_command_line

def run():
    execute_from_command_line([sys.argv[0], 'test', 'accounts'])
    execute_from_command_line([sys.argv[0], 'test', 'core'])
    execute_from_command_line([sys.argv[0], 'test', 'leaderboard'])

if __name__ == "__main__":
    run()
