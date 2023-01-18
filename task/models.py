
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .querysets import TaskQuerySet

User = get_user_model()


class Task(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "PEN", _("Pending task")
        DUE = "DUE", _("Due task")
        COMPLETED = "COM", _("Completed task")


    class PriorityChoices(models.TextChoices):
        URGENT = "URG", _("Urgent priority")
        HIGH = "HGH", _("High priority")
        NORMAL = "NRM", _("Normal priority")
        LOW = "LOW", _("Low priority")


    created_by = models.ForeignKey(
        verbose_name=_("Task created by user"),
        to=User,
        on_delete=models.SET_NULL,
        related_name='user_created_tasks',
        null=True,
        blank=True,
    )
    assign_to = models.ForeignKey(
        verbose_name=_("Task assign to"),
        to=User,
        on_delete=models.CASCADE,
        related_name='user_tasks',
    )
    title = models.CharField(
        verbose_name=_("Task title"),
        max_length=200,
    )
    description = models.TextField(
        verbose_name=_("Task description")
    )
    created_at = models.DateTimeField(
        verbose_name=_("Task creation time"),
        auto_now_add=True,
    )
    last_date = models.DateTimeField(
        verbose_name=_("Task submission dadeline")
    )
    approved_by_dept_head = models.BooleanField(
        verbose_name=_("Approved by department head"),
        default=False
    )
    status = models.CharField(
        verbose_name=_("Task status"),
        max_length=3,
        choices=StatusChoices.choices,
    )
    priority = models.CharField(
        verbose_name=_("Task priority"),
        max_length=3,
        choices=PriorityChoices.choices,
    )
    objects = TaskQuerySet.as_manager()






