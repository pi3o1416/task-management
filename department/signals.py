
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import DepartmentMember, Department, Designations
from . import tasks


@receiver(signal=pre_save, sender=DepartmentMember)
def fill_department_designation_user_info(sender, instance, **kwargs):
    instance.department_name = instance.department.name
    instance.designation_title = instance.designation.title
    return instance


@receiver(signal=post_save, sender=Department)
def cache_department_info(sender, instance, **kwargs):
    tasks.cache_department.delay()


@receiver(signal=post_save, sender=Designations)
def cache_designation_info(sender, instance, **kwargs):
    tasks.cache_designation.delay()

