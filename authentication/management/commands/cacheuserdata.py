
from django.utils.translation import gettext_lazy as _
from django.core.management.base import BaseCommand, CommandError
from ...tasks import cache_users_data


class Command(BaseCommand):
    help = 'Cache users data'

    def handle(self, *args, **kwargs):
        try:
            cache_users_data.delay()
        except Exception as exception:
            raise CommandError(exception.__str__())

