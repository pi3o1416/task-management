
from django.core.cache import cache
from celery import shared_task
from .models import Department, Designations


@shared_task(name='cache_department')
def cache_department():
    departments = Department.objects.all().values('pk', 'name', 'description')
    departments_data = {department['pk']: department for department in departments}
    cache.set('departments', departments_data, timeout=3600*6.5)


@shared_task(name='cache_designation')
def cache_designation():
    designations = Designations.objects.all().values('pk', 'department', 'title')
    designations_data = {designation['pk']: designation for designation in designations}
    cache.set('designations', designations_data, timeout=3600*6.5)



