from django.core.management.base import BaseCommand
import time
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Auto backup every 30 minutes'

    def handle(self, *args, **options):
        while True:
            time.sleep(7200)
            call_command("dbbackup")
