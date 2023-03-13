
from django.core.cache import cache
from celery import shared_task
from .models import Team


@shared_task(name='cache_teams')
def cache_teams():
    teams = Team.objects.all().values('pk', 'title', 'description', 'department', 'team_lead')
    team_data = {team['pk']: team for team in teams}
    cache.set('teams', team_data, timeout=3600*6.5)




