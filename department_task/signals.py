
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from task.models import Task
from .models import DepartmentTask


@receiver(signal=post_save, sender=DepartmentTask)
def update_task_type_to_dept_task(sender, instance:DepartmentTask, created, **kwargs):
    if created:
        task = instance.task
        task.update(task_type=Task.TaskType.DEPARTMENT_TASK)


@receiver(signal=post_delete, sender=DepartmentTask)
def update_task_type_to_undermine(sender, instance:DepartmentTask, **kwargs):
    task = instance.task
    task.update(task_type=Task.TaskType.NONE)



