
from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import DepartmentMember


@receiver(signal=pre_save, sender=DepartmentMember)
def fill_department_designation_user_info(sender, instance, **kwargs):
    instance.department_name = instance.department.name
    instance.member_full_name = instance.member.full_name
    instance.designation_title = instance.designation.title
    return instance











