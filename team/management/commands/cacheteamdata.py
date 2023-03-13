
from django.core.management import BaseCommand, CommandError
from ...tasks import cache_teams


class Command(BaseCommand):
    help = 'Cache users data'

    def handle(self, *args, **kwargs):
        try:
            cache_teams.delay()
        except Exception as exception:
            raise CommandError(exception.__str__())











