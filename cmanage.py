#!/usr/bin/env python
import os
import sys

from killdb import kill

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monkeyladder.settings.production")

    from django.core.management import execute_from_command_line

    fixtures = ['fixtures/core.json', 'fixtures/leaderboard.json']
    if len(sys.argv) > 1:
        if sys.argv[1] == "newdb":
            kill()
            execute_from_command_line([sys.argv[0], 'syncdb', '--noinput'])
            execute_from_command_line([sys.argv[0], 'loaddata'] + fixtures)
            exit(0)
            
    execute_from_command_line(sys.argv)
        