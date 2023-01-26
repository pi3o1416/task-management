
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from .models import UsersTasks, Task, TaskTree

@receiver(signal=pre_save, sender=UsersTasks)
def fill_users_tasks_user_info(sender, instance, **kwargs):
    instance.user_username = instance.assigned_to.username
    instance.user_full_name = instance.assigned_to.full_name
    return instance


@receiver(signal=pre_save, sender=Task)
def fill_task_created_by_user_info(sender, instance, update_fields=None, **kwargs):
    if update_fields == None:
        instance.created_by_user_username = instance.created_by.username
        instance.created_by_user_fullname = instance.created_by.full_name
        return instance


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







