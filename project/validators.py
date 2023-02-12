
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

from task.models import Task

User = get_user_model()


def validate_project_deadline(deadline):
    """
    Validate if deadline is greater than today
    """
    today = timezone.now().date()
    if deadline <= today:
        raise ValidationError(message="Project deadline should be greater than current date")
    return deadline


def validate_budget(budget):
    """
    Validate if budget is less than 0
    """
    if budget < 0:
        raise ValidationError(message="Budget should not be less than 0")
    return budget


def validate_project_manager_permission(project_manager):
    if not isinstance(project_manager, User):
        project_manager = User.objects.get_user_by_pk(pk=project_manager)
    if project_manager.has_perm('project.can_maintain_project') == True:
        return project_manager
    raise ValidationError(message="Project manager does not have permission to maintain project")


def validate_project_owner_permission(project_owner):
    if not isinstance(project_owner, User):
        project_owner = User.objects.get_user_by_pk(pk=project_owner)
    if project_owner.has_perm('project.can_own_project') == True:
        return project_owner
    raise ValidationError(message="Project owner does not have permission to own project")

def validate_project_task_type(project_task):
    if not isinstance(project_task, Task):
        project_task = Task.objects.get_task_by_pk(project_task)
    if project_task.task_type == Task.TaskType.PROJECT_TASK:
        return project_task
    raise ValidationError(message="Task type should be project task")



