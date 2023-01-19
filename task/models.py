
import os
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .querysets import TaskQuerySet, TaskAttachmentsQuerySet, TaskTreeQuerySet, UsersTasksQuerySet
from .exceptions import DBOperationFailed

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
    created_by_user_username = models.CharField(
        verbose_name = _("Created by user  username"),
        max_length=100,
        blank=True,
        null=True,
    )
    created_by_user_fullname = models.CharField(
        verbose_name=_("Created by user full name"),
        max_length=200,
        blank=True,
        null=True
    )
    objects = TaskQuerySet.as_manager()

    class Meta:
        permissions = (("can_approve_disapprove_task", _("Can Approve Or Disapprove Tasks")),)


    def __str__(self):
        return self.title

    def approve_task(self):
        self.approved_by_dept_head = True
        self.save()
        return True

    def disapprove_task(self):
        self.approved_by_dept_head = False
        self.save()
        return True

    def _change_task_status(self, status):
        try:
            if self.status == status:
                return True
            self.status = status
            self.save()
            return True
        except Exception as exception:
            raise DBOperationFailed(detail={"detail": exception.args})


    def mark_task_as_complete(self):
        return self._change_task_status(self.StatusChoices.COMPLETED)

    def mark_task_as_due(self):
        return self._change_task_status(self.StatusChoices.DUE)

    def mark_task_as_pending(self):
        return self._change_task_status(self.StatusChoices.PENDING)


class UsersTasks(models.Model):
    assigned_to = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='user_tasks',
        verbose_name=_("User")
    )
    task = models.OneToOneField(
        to=Task,
        on_delete=models.CASCADE,
        related_name='task_assigned_to',
        verbose_name=_("Task"),
    )
    user_username = models.CharField(
        verbose_name=_("User username"),
        max_length=200,
        blank=True,
        null=True,
    )
    user_full_name = models.CharField(
        verbose_name=_("User fullname"),
        max_length=200,
        blank=True,
        null=True,
    )
    objects = UsersTasksQuerySet.as_manager()

    class Meta:
        permissions = (("can_view_inter_department_task", _("Can View Inter Department Tasks")),
                       ("can_view_all_tasks", _("Can View All Tasks")))



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


class TaskTree(models.Model):
    parent = models.ForeignKey(
        to=Task,
        verbose_name=_("Task parent"),
        related_name='task_childs',
        on_delete=models.CASCADE,
    )
    child = models.OneToOneField(
        to=Task,
        verbose_name=_("Task child"),
        related_name='task_parent',
        on_delete=models.CASCADE
    )
    objects = TaskTreeQuerySet.as_manager()



















