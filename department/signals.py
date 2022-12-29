
from rest_framework.exceptions import NotAcceptable
from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import DepartmentMember


@receiver(signal=pre_save, sender=DepartmentMember)
def fill_department_designation_user_info(sender, instance, **kwargs):
    instance.department_name = instance.department.name
    instance.member_full_name = instance.member.full_name
    instance.designation_title = instance.designation.title
    return instance

@receiver(signal=pre_save, sender=DepartmentMember)
def test_designation_from_same_department(sender, instance, **kwargs):
    department = instance.department
    designation_department = instance.designation.department
    if department != designation_department:
        raise NotAcceptable({"detail": ["Member department and department designation did not match."]})










