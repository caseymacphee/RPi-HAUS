from django.core.management.base import BaseCommand
from haus.cron_jobs import daily_summary_cron

class Command(BaseCommand):
    args = ''
    help = 'Creates daily summary entries from data'

    def handle(self, *args, **options):
        daily_summary_cron()

        self.stdout.write("Successfully digested yesterday's data")
