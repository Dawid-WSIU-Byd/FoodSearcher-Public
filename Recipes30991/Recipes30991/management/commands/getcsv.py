from django.core.management.base import BaseCommand
from main.views import get_csv


class Command(BaseCommand):
    help = 'Gets data from CSV file'

    def handle(self, *args, **options):
        get_csv()
        self.stdout.write(self.style.SUCCESS('Successfully imported data from CSV'))
