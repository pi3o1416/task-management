
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from .models import UsersTasks, Task

@receiver(signal=pre_save, sender=UsersTasks)
def fill_users_tasks_user_info(sender, instance, **kwargs):
    instance.user_username = instance.assigned_to.username
    instance.user_full_name = instance.assigned_to.full_name
    return instance


@receiver(signal=post_save, sender=Task)
def fill_task_created_by_user_info(sender, instance, created, **kwargs):
    if created:
        instance.created_by_user_username = instance.created_by.username
        instance.created_by_user_fullname = instance.created_by.full_name
        instance.save()

















