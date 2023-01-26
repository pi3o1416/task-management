
from io import DEFAULT_BUFFER_SIZE
import os
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .querysets import TaskQuerySet, TaskAttachmentsQuerySet, TaskTreeQuerySet, UsersTasksQuerySet
from .exceptions import DBOperationFailed, InvalidRequest

User = get_user_model()


class Task(models.Model):
    #TODO: validate last_date
    class StatusChoices(models.TextChoices):
        PENDING = "PEN", _("Pending task")
        DUE = "DUE", _("Due task")
        COMPLETED = "COM", _("Completed task")
        SUBMITTED = "SUB", _("Sumitted Task")


    class PriorityChoices(models.TextChoices):
        URGENT = "URG", _("Urgent priority")
        HIGH = "HGH", _("High priority")
        NORMAL = "NRM", _("Normal priority")
        LOW = "LOW", _("Low priority")


    class ApprovalChoices(models.TextChoices):
        APPROVED = "APP", _("Approved")
        PENDING = "PEN", _("Pending")
        REJECTED = "REJ", _("Rejected")


    class TaskType(models.TextChoices):
        NONE = "NON", _("Type not yet fixed")
        USER_TASK = "RGT", _("Regular task")
        DEPARTMENT_TASK = "DPT", _("Department task")
        PROJECT_TASK = "PRT", _("Project task")
        TEAM_TASK = "TMT", _("Team task")

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
    approval_status = models.CharField(
        verbose_name=_("Task approval by department head"),
        max_length=3,
        choices=ApprovalChoices.choices,
        default=ApprovalChoices.PENDING
    )
    status = models.CharField(
        verbose_name=_("Task status"),
        max_length=3,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )
    priority = models.CharField(
        verbose_name=_("Task priority"),
        max_length=3,
        choices=PriorityChoices.choices,
        default=PriorityChoices.LOW,
    )
    task_type = models.CharField(
        verbose_name=_("Task type"),
        max_length=3,
        choices=TaskType.choices,
        default=TaskType.NONE
    )
    is_assigned = models.BooleanField(
        verbose_name=_("Is task already assigned"),
        default=False
    )
    has_subtask = models.BooleanField(
        verbose_name=_("Task has any subtask"),
        default=False,
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
        permissions = (("can_approve_disapprove_task", _("Can Approve Or Disapprove Tasks")),
                       ("can_view_all_tasks", _("Can View All Tasks")))

    def __str__(self):
        return self.title

    @classmethod
    def create_factory(cls, commit, **kwargs):
        try:
            assert kwargs.get("title") != None, "Task title is required"
            assert kwargs.get("description") != None, "Task description is required"
            assert kwargs.get("last_date") != None, "Task submission last date is required"
            assert kwargs.get("priority") != None, "Task priority is required"
            task = cls(**kwargs)
            if commit == True:
                task.save()
            return task
        except AssertionError as exception:
            raise InvalidRequest(detail={"detail": _(exception.__str__())})
        except Exception as exception:
            raise DBOperationFailed(detail={"detail": _(exception.__str__())})

    def delete(self):
        if self.approval_status == self.ApprovalChoices.APPROVED:
            raise InvalidRequest(detail={"detail": _("Task that is approved by department head can not be deleted")})
        return super().delete()

    def approve_task(self):
        if self.approval_status == self.ApprovalChoices.APPROVED:
            raise InvalidRequest(detail={"detail": _("Task has already been approved by department head")})
        self.approval_status = self.ApprovalChoices.APPROVED
        self.save(update_fields=['approval_status'])
        return True

    def reject_approval_request(self):
        if self.approval_status == self.ApprovalChoices.REJECTED:
            raise InvalidRequest(detail={"detail": _("Task has already been rejected by department head")})
        self.approval_status = self.ApprovalChoices.REJECTED
        self.save(update_fields=['approval_status'])
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

    def update_task_owner(self, user, commit=True):
        assert type(user) is User, "Please Provide a valid user instance"
        self.created_by = user
        if commit:
            self.save()

    def accept_task_submission(self):
        if self.status == self.StatusChoices.SUBMITTED:
            return self._change_task_status(self.StatusChoices.COMPLETED)
        raise InvalidRequest(detail={"detail": _("Submit the task before mark it as complete")})

    def reject_task_submission(self):
        if self.status == self.StatusChoices.SUBMITTED:
            return self._change_task_status(self.StatusChoices.DUE)
        raise InvalidRequest(detail={"detail": _("Submit the task before reject it.")})

    def start_task(self):
        if self.status == self.StatusChoices.PENDING:
            return self._change_task_status(self.StatusChoices.DUE)
        raise InvalidRequest(detail={"detail": _("Cannot start a task that has been already started")})

    def submit_task(self):
        if self.status == self.StatusChoices.DUE:
            return self._change_task_status(self.StatusChoices.SUBMITTED)
        raise InvalidRequest(detail={"detail": _("Start the task before submit it")})


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
                       ("can_view_all_users_tasks", _("Can View All Users Tasks")))


    @classmethod
    def create_factory(cls, commit=False, **kwargs):
        try:
            assert kwargs.get("task") != None, "Task should not be empty"
            assert kwargs.get("assigned_to") != None, "Task assigned_to field should not be empty"
            user_task = cls(**kwargs)
            if commit == True:
                user_task.save()
            return user_task
        except AssertionError as exception:
            raise InvalidRequest(detail={"detail": _(exception.__str__())})
        except Exception as exception:
            raise InvalidRequest(detail={"detail": _(exception.__str__())})


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
        verbose_name=_("Task")
    )
    attached_by = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name='user_files',
        verbose_name=_("Attached by"),
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

    @classmethod
    def create_factory(cls, commit=False, **kwargs):
        try:
            assert kwargs.get("task") != None, "Task should not be empty"
            assert kwargs.get("attachment") != None, "Attachment should not be empty"
            assert isinstance(kwargs.get("attached_by"), User), "Please provide a valid user"
            task_attachment = cls(**kwargs)
            if commit == True:
                task_attachment.save()
            return task_attachment
        except AssertionError as exception:
            breakpoint()
            raise InvalidRequest(detail={"detail": _(exception.__str__())})
        except Exception as exception:
            breakpoint()
            raise InvalidRequest(detail={"detail": _(exception.__str__())})

    def delete(self):
        try:
            super().delete()
            return True
        except Exception as exception:
            raise DBOperationFailed(detail={"detail": _(exception.__str__())})

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

    @classmethod
    def create_factory(cls, commit=False, **kwargs):
        try:
            assert kwargs.get("parent") != None, "Parent should not be empty"
            assert kwargs.get("child") != None, "Child should not be empty"
            task_tree = cls(**kwargs)
            if commit == True:
                task_tree.save()
            return task_tree
        except AssertionError as exception:
            raise InvalidRequest(detail={"detail": _(exception.__str__())})
        except Exception as exception:
            raise InvalidRequest(detail={"detail": _(exception.__str__())})










