
from django.core.cache import cache
from celery import shared_task
from .models import Project


@shared_task(name='cache_projects')
def cache_projects():
    projects = Project.objects.all().values('pk', 'title', 'description', 'deadline', 'budget',
                                            'project_manager', 'project_owner', 'department',
                                            'status')
    project_data = {project['pk']: project for project in projects}
    cache.set('projects', project_data, timeout=3600*6.5)

