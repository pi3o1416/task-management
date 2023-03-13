
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import CustomUser
from . import tasks


@receiver(signal=post_save, sender=CustomUser)
def send_account_activation_email(sender, instance, created, **kwargs):
    if created:
        instance.send_account_active_email()


@receiver(signal=post_save, sender=CustomUser)
def cache_users_data(sender, instance, **kwargs):
    tasks.cache_users_data.delay()

















