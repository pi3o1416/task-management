
from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

from services.decorators import is_authenticated
from .models import DepartmentMember, Department


User = get_user_model()


class IsSameDepartment(BasePermission):
    message = "Requested user and retrieved user does not belong in same department"
    @is_authenticated
    def has_object_permission(self, request, view, obj:User):
        department_members = DepartmentMember.objects.filter(member__in=[request.user.pk, obj.pk])
        if department_members.is_members_department_same():
            return True
        return False


class IsBelongToDepartment(BasePermission):
    message = "Requested user does not belong to this department"
    @is_authenticated
    def has_object_permission(self, request, view, department:Department):
        user = request.user
        if DepartmentMember.objects.member_department(member_pk=user.pk) == department.pk:
            return True
        return False


