
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django_celery_results.models import TaskResult

from .querysets import EmailHistoryQuerySet

# Create your models here.

class EmailHistory(models.Model):
    class EmailStatus(models.TextChoices):
        SUCCESS = 'SUC', _("Email Success")
        FAILURE = 'FIL', _("Email Failure")
        STARTED = 'STR', _("Email Send Started")

    email_task = models.OneToOneField(
        verbose_name=_("Email Core"),
        to=TaskResult,
        on_delete=models.CASCADE,
        related_name='email',
        null=True,
        blank=True,
    )
    email_subject = models.CharField(
        verbose_name=_("Email Subject"),
        max_length=200,
    )
    email_body = models.TextField(
        verbose_name=_("Email Body")
    )
    email_to = models.CharField(
        verbose_name="Email To",
        max_length=1000
    )
    created_at = models.DateTimeField(
        verbose_name=_("Email Sending Time"),
        auto_now_add=True,
    )
    email_status = models.CharField(
        verbose_name="Email Status",
        max_length=3,
        choices=EmailStatus.choices
    )
    email_manager = EmailHistoryQuerySet.as_manager()

    class Meta:
        ordering = ['created_at']







