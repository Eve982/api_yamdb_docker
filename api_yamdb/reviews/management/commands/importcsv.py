from django.core.management.base import BaseCommand, CommandError
from reviews.management.commands._utils import get_data


class Command(BaseCommand):
    help = 'Import csv data from /static/data/ in database'

    def handle(self, *args, **options):
        get_data()
