
from django.core.cache import cache
from celery import shared_task
from .models import CustomUser


@shared_task(name='cache_users_data')
def cache_users_data():
    users = CustomUser.objects.all().values(*CustomUser.CACHED_FIELDS)
    user_dict = {user["pk"]: user for user in users}
    cache.set('users', user_dict, timeout=3600*6.5)


