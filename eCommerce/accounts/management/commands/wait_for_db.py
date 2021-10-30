"""
Django command to wait for the database to be available.
"""
# Colors
ENDC = '\033[0m'
WARNING = '\033[93m'
OKGREEN = '\033[92m'
OKCYAN = '\033[96m'
FAIL = '\033[91m'

import time
from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        # ToDo: Colorize this lines
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write(FAIL + 'Database unavailable, waiting 1 second...' + ENDC)
                time.sleep(1)

        self.stdout.write(OKGREEN + self.style.SUCCESS('Database available!') + ENDC)

