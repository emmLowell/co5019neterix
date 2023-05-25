#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv


def setup_config(production: bool = False):
    if production:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.Neterix.settings")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.Neterix.settings_dev")


def run_server(args=None, production=False):
    """Run administrative tasks."""
    setup_config(production=production)
    from django.core.management import execute_from_command_line

    if args is None or len(args) == 0:
        execute_from_command_line(["manage.py", "runserver", "0.0.0.0:8080"])
    else:
        to_run = ["manage.py"]
        to_run.extend(args)
        execute_from_command_line(argv=to_run)


if __name__ == "__main__":
    load_dotenv()
    run_server()
