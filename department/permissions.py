
from rest_framework.permissions import BasePermission

from services.decorators import is_authenticated
from .models import DepartmentMember




class IsSameDepartment(BasePermission):
    @is_authenticated
    def has_object_permission(self, request, view, obj):
        department_members = DepartmentMember.objects.filter(member__in=[request.user.pk, obj.pk])
        if department_members.is_members_department_same():
            return True
        return False


