
from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import UsersTasks

@receiver(signal=pre_save, sender=UsersTasks)
def fill_users_tasks_user_info(sender, instance, **kwargs):
    instance.user_username = instance.assigned_to.username
    instance.user_full_name = instance.assigned_to.full_name
    return instance















