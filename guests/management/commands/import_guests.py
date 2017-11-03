from django.core.management import BaseCommand
from guests import csv_import


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('filename',  nargs='+', type=str)

    def handle(self, *args, **options):
        csv_import.import_guests(options['filename'][0])
