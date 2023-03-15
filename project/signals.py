
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.forms import model_to_dict
from django.db.models.signals import post_save, post_delete

from task.models import Task
from .models import Project, ProjectTask
from . import tasks


@receiver(signal=post_save, sender=Project)
def add_project_manager_as_project_member(sender, instance:Project, created=None, update_fields=None, **kwargs):
    if created:
        project_manager = instance.project_manager
        instance.members.add(project_manager)


@receiver(signal=post_save, sender=Project)
def cache_projects_data(sender, instance, **kwargs):
    tasks.cache_projects.delay()


@receiver(signal=post_save, sender=ProjectTask)
def update_task_type_to_project_task(sender, instance, created, **kwargs):
    if created:
        task_pk = model_to_dict(instance=instance, fields=['task']).get('task')
        Task.objects.filter(pk=task_pk).update(task_type=Task.TaskType.PROJECT_TASK)


@receiver(signal=post_delete, sender=ProjectTask)
def update_task_type_to_user_task(sender, instance, **kwargs):
    task_pk = model_to_dict(instance=instance, fields=['task']).get('task')
    Task.objects.filter(pk=task_pk).update(task_type=Task.TaskType.USER_TASK)

