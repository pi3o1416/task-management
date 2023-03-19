
from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from rest_framework.permissions import BasePermission

from services.decorators import is_authenticated, has_kperms
from .models import Task, UsersTasks


User = get_user_model()


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
    message = "You are not task owner"
    @is_authenticated
    def has_object_permission(self, request, view, user_task:UsersTasks):
        created_by = model_to_dict(user_task.task, fields=['created_by']).get('created_by')
        if request.user.pk == created_by:
            return True
        return False


class IsTaskOwner(BasePermission):
    message = "You are not task owner"
    @is_authenticated
    def has_object_permission(self, request, view, task:Task):
        user = request.user
        task_created_by_pk = model_to_dict(task, fields=['created_by']).get('created_by')
        if task_created_by_pk == user.pk:
            return True
        return False

class IsTaskAssignee(BasePermission):
    message = "You are not task assignee"
    @is_authenticated
    def has_object_permission(self, request, view, task:Task):
        user = request.user
        if task.task_type == Task.TaskType.USER_TASK:
            assignee_pk = UsersTasks.objects.values_list('assigned_to', flat=True).get(task=task)
            if user.pk == assignee_pk:
                return True
        return False


class IsTaskParents(BasePermission):
    message = "You are not one of the creator of parent tasks"
    @is_authenticated
    def has_object_permission(self, request, view, task:Task):
        user = request.user
        parent_tasks_owners = Task.objects.values_list('created_by', flat=True) \
            .filter(pk__in=task.parent_tasks)
        if user.pk in parent_tasks_owners:
            return True
        return False


class IsAttachmentOwner(BasePermission):
    message = "You are not owner of this attachment"
    @is_authenticated
    def has_object_permission(self, request, view, attachment):
        user = request.user
        if user.pk == model_to_dict(attachment).get('attached_by'):
            return True
        return False


class CanManageExistingTask(BasePermission):
    message = "You do not have permission to manage this task"
    @is_authenticated
    def has_object_permission(self, request, view, task):
        if task.task_type == Task.TaskType.USER_TASK and task.created_by_id == request.user.pk:
            return True
        if task.task_type == Task.TaskType.DEPARTMENT_TASK:
            if request.user.has_perm('department_task.can_manage_department_task'):
                task_dept = task.assigned_to_dept.department_id
                user_dept = request.user.user_department.department_id
                if task_dept == user_dept:
                    return True
        if task.task_type == Task.TaskType.PROJECT_TASK:
            if task.created_by_id == request.user.pk:
                return True
            task_project = task.task_project
            user_in_task_project = request.user.user_projects.filter(pk=task_project.pk).exists()
            if user_in_task_project == True and request.user.has_perm('project.can_maintain_project'):
                return True
        if task.task_type == Task.TaskType.TEAM_TASK:
            if task.created_by_id == request.user.pk:
                return True
            task_team = task.task_team
            user_in_task_team = request.user.teams.filter(pk=task_team.pk).exists()
            if user_in_task_team == True and request.user.has_perm('team.can_manage_team_tasks'):
                return True
        return False



