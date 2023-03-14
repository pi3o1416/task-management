
from django.forms import model_to_dict
from rest_framework.permissions import BasePermission

from services.decorators import is_authenticated, has_kperms
from .models import Task, UsersTasks


@has_kperms(['task.can_view_all_tasks'])
class CanViewAllTasks(BasePermission):
    message = 'You do not have permission to view all tasks'


@has_kperms(['task.add_task'])
class CanCreateTask(BasePermission):
    message = 'You do not have permission to add task'


@has_kperms(['task.delete_task'])
class CanDeleteTask(BasePermission):
    message = 'You do not have permission to delete task'


@has_kperms(['task.change_task'])
class CanUpdateTask(BasePermission):
    message = 'You do not have permission to change task'


@has_kperms(['task.can_approve_disapprove_task'])
class HasPermissionToApproveTask(BasePermission):
    message = 'You do not have permission to approve or disapprove task'


@has_kperms(['task.can_view_inter_department_task'])
class CanViewInterDepartmentTask(BasePermission):
    message = 'You do not have permission to view inter department task'


@has_kperms(['task.add_userstasks'])
class CanCreateUsersTasks(BasePermission):
    message = 'You do not have permission to assign user any task'


class IsUserTaskOwner(BasePermission):
    @is_authenticated
    def has_object_permission(self, request, view, user_task:UsersTasks):
        created_by = model_to_dict(user_task.task, fields=['created_by']).get('created_by')
        if request.user.pk == created_by:
            return True
        return False


class IsTaskOwner(BasePermission):
    @is_authenticated
    def has_object_permission(self, request, view, task:Task):
        user = request.user
        task_created_by_pk = model_to_dict(task, fields=['created_by']).get('created_by')
        if task_created_by_pk == user.pk:
            return True
        return False

class IsTaskAssignee(BasePermission):
    @is_authenticated
    def has_object_permission(self, request, view, task:Task):
        user = request.user
        if task.task_type == Task.TaskType.USER_TASK:
            assignee_pk = UsersTasks.objects.values_list('assigned_to', flat=True).get(task=task)
            if user.pk == assignee_pk:
                return True
        return False


class IsTaskParents(BasePermission):
    @is_authenticated
    def has_object_permission(self, request, view, task:Task):
        user = request.user
        parent_tasks_owners = Task.objects.values_list('created_by', flat=True) \
            .filter(pk__in=task.parent_tasks)
        if user.pk in parent_tasks_owners:
            return True
        return False


class IsAttachmentOwner(BasePermission):
    @is_authenticated
    def has_object_permission(self, request, view, attachment):
        user = request.user
        if user.pk == model_to_dict(attachment).get('attached_by'):
            return True
        return False




