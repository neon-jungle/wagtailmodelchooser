#!/usr/bin/env python

import os
import sys


def run():
    from django.core.management import execute_from_command_line

    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    run()
