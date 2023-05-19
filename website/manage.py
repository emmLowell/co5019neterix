#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv


def setup_config():
    production = os.getenv("PRODUCTION", "false").lower() == "true"
    if (production):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.Neterix.settings')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.Neterix.settings_dev')


def run_server():
    """Run administrative tasks."""
    setup_config()
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    load_dotenv()
    run_server()
