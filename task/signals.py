
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import UsersTasks, Task, TaskTree

@receiver(signal=post_save, sender=UsersTasks)
def change_task_type_and_assignment_status(sender, instance, created, **kwargs):
    if created:
        task = instance.task
        task.is_assigned=True
        task.task_type = Task.TaskType.USER_TASK
        task.save(update_fields=['is_assigned', 'task_type'])


@receiver(signal=post_save, sender=TaskTree)
def update_has_subtask_fields_of_task_instance(sender, instance, created, **kwargs):
    pass







