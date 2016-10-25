#!/usr/bin/env python

import os
import sys


def run():
    from django.core.management import execute_from_command_line
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    os.environ.setdefault('DATABASE_NAME', ':memory:')
    execute_from_command_line([sys.argv[0], 'test'] + sys.argv[1:])


if __name__ == '__main__':
    run()
