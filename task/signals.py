
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import TaskTree

@receiver(signal=post_save, sender=TaskTree)
def update_has_subtask_fields_of_task_instance(sender, instance, created, **kwargs):
    pass







