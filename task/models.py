
import os
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .querysets import TaskQuerySet, TaskAttachmentsQuerySet

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

    def __str__(self):
        return self.title


def task_attachment_upload_path(instance, filename):
    file_path = 'task-attachments/{}/{}'.format(instance.task.pk, filename)
    desired_path = os.path.join(settings.MEDIA_ROOT, file_path)
    name, extension = os.path.splitext(filename)
    counter = 1
    while os.path.exists(desired_path) == True:
        file_path = 'task-attachments/{}/{}_{}{}'.format(instance.task.pk, name, counter, extension)
        desired_path = os.path.join(settings.MEDIA_ROOT, file_path)
        counter += 1
    return file_path


class TaskAttachments(models.Model):
    task = models.ForeignKey(
        to=Task,
        on_delete=models.CASCADE,
        related_name='task_attachments',
        verbose_name=_("Task attachments")
    )
    attached_by = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name='user_files',
        verbose_name=_("Task attachments"),
        blank=True,
        null=True,
    )
    attachment = models.FileField(
        verbose_name=_("Task attachment"),
        upload_to=task_attachment_upload_path
    )
    attached_at = models.DateTimeField(
        verbose_name=_("File attached at"),
        auto_now_add=True
    )
    objects = TaskAttachmentsQuerySet.as_manager()












