
from django.forms import model_to_dict
from rest_framework.permissions import BasePermission

from services.decorators import is_authenticated, has_kperms
from .models import Task, UsersTasks


@has_kperms(['task.can_view_all_tasks'])
class CanViewAllTasks(BasePermission):
    pass


@has_kperms(['task.add_task'])
class CanCreateTask(BasePermission):
    pass


@has_kperms(['task.delete_task'])
class CanDeleteTask(BasePermission):
    pass


@has_kperms(['task.change_task'])
class CanUpdateTask(BasePermission):
    pass


@has_kperms(['task.can_approve_disapprove_task'])
class HasPermissionToApproveTask(BasePermission):
    pass


class IsTaskOwner(BasePermission):
    @is_authenticated
    def has_object_permission(self, request, view, task:Task):
        user = request.user
        if task.created_by == user:
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




