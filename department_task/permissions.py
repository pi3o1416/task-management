
from django.forms import model_to_dict
from rest_framework.permissions import BasePermission

from department.models import DepartmentMember
from services.decorators import has_kperms, is_authenticated
from .models import DepartmentTask


@has_kperms(['department_task.add_departmenttask'])
class CanCreateDepartmentTask(BasePermission):
    message = 'You do not have permission to create department task.'
    pass


@has_kperms(['department_task.can_manage_departmnet_task'])
class CanManageDepartmentTask(BasePermission):
    message = 'You do not have permission to manage department task.'
    pass


class IsDepartmentTaskOwner(BasePermission):
    message = "Your are not department task owner"
    @is_authenticated
    def has_object_permission(self, request, view, obj:DepartmentTask):
        task = obj.task
        if request.user == model_to_dict(task).get('created_by'):
            return True
        return False


class IsBelongToDepartmentTaskDepartment(BasePermission):
    message = "You do not belong to department task assigned department"
    @is_authenticated
    def has_object_permission(self, request, view, obj:DepartmentTask):
        user = request.user
        user_department = DepartmentMember.objects.member_department(member_pk=user.pk)
        department_task_department = model_to_dict(obj, fields=['department']).get('department')
        if department_task_department == user_department:
            return True
        return False

