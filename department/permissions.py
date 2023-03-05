
from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

from services.decorators import is_authenticated
from .models import DepartmentMember, Department


User = get_user_model()


class IsSameDepartment(BasePermission):
    @is_authenticated
    def has_object_permission(self, request, view, obj:User):
        department_members = DepartmentMember.objects.filter(member__in=[request.user.pk, obj.pk])
        if department_members.is_members_department_same():
            return True
        return False


class IsBelongToDepartment(BasePermission):
    @is_authenticated
    def has_object_permission(self, request, view, obj:Department):
        user = request.user
        if user.user_department == obj:
            return True
        return False


