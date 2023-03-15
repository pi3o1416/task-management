
from django.forms import model_to_dict
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from task.models import Task
from .models import DepartmentTask


@receiver(signal=post_save, sender=DepartmentTask)
def update_task_type_to_dept_task(sender, instance:DepartmentTask, created, **kwargs):
    if created:
        task_pk = model_to_dict(instance=instance, fields=['task'])
        Task.objects.filter(pk=task_pk).update(task_type=Task.TaskType.DEPARTMENT_TASK)


@receiver(signal=post_delete, sender=DepartmentTask)
def update_task_type_to_user_task(sender, instance:DepartmentTask, **kwargs):
    task_pk = model_to_dict(instance=instance, fields=['task'])
    Task.objects.filter(pk=task_pk).update(task_type=Task.TaskType.USER_TASK)



