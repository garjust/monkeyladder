#!/usr/bin/env python
import os
import sys

from django.core.management import execute_from_command_line

FIXTURES = ['fixtures/users.json', 'fixtures/ladders.json', 'fixtures/leaderboard.json']


def save_fixture(target, *apps):
    sys.stdout = open(target, 'w')
    execute_from_command_line([sys.argv[0], 'dumpdata'] + list(apps) + ['--indent', '2'])
    sys.stdout.close()
    sys.stdout = sys.__stdout__


def migrate(target='fixtures'):
    save_fixture('%s/users.json' % target, 'auth.User')
    save_fixture('%s/ladders.json' % target, 'ladders', '-e', 'ladders.LadderConfigurationKey')
    save_fixture('%s/leaderboard.json' % target, 'leaderboard')
    #ssave_fixture('%s/comments.json' % target, 'comments')

if __name__ == '__main__':
    sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))
    os.chdir(os.path.abspath(os.path.join(__file__, '..', '..', 'monkeyladder')))

    migrate()
