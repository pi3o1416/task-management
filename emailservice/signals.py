
from django.dispatch import receiver
from django.db.models.signals import post_save
from django_celery_results.models import TaskResult
from .models import EmailHistory
from .services import get_args_from_task_kwargs


#@receiver(signal=post_save, sender=TaskResult)
#def create_new_history(sender, instance, created, **kwargs):
#    print('triggered')
#    if created:
#        email_subject, email_body, email_to = get_args_from_task_args(instance.task_kwargs)
#        for email in email_to:
#            email = EmailHistory.email_manager.create(
#                email_task=instance,
#                email_subject=email_subject,
#                email_body=email_body,
#                email_to=email,
#                email_status=getattr(EmailHistory.EmailStatus, instance.status)
#            )
#            email.save()
#    else:
#        email = EmailHistory.email_manager.get(email_task=instance)
#        email.email_status=getattr(EmailHistory.EmailStatus, instance.status)
#        email.save()











