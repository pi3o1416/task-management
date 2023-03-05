
from django.forms import model_to_dict
from rest_framework.permissions import BasePermission

from services.decorators import has_kperms, is_authenticated
from .models import DepartmentTask


@has_kperms(['department_task.can_create_department_task'])
class CanCreateDepartmentTask(BasePermission):
    pass


@has_kperms(['department_task.can_manage_departmnet_task'])
class CanManageDepartmentTask(BasePermission):
    pass


class IsDepartmentTaskOwner(BasePermission):
    @is_authenticated
    def has_object_permission(self, request, view, obj:DepartmentTask):
        task = obj.task
        if request.user == model_to_dict(task).get('created_by'):
            return True
        return False


class IsBelongToDepartmentTaskDepartment(BasePermission):
    @is_authenticated
    def has_object_permission(self, request, view, obj:DepartmentTask):
        user = request.user
        if model_to_dict(obj).get('department') == user.user_department.pk:
            return True
        return False

