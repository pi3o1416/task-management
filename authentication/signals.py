
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import CustomUser


@receiver(signal=post_save, sender=CustomUser)
def send_account_activation_email(sender, instance, created, **kwargs):
    if created:
        instance.send_account_active_email()

















