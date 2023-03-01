
import os
from operator import __and__

from django.forms import model_to_dict
from django.db import connection
from django.db import models
from django.db import IntegrityError
from django.db.models import Count, OuterRef, Subquery
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from department.models import DepartmentMember
from services.querysets import get_model_foreignkey_fields
from services.querysets import TemplateQuerySet
from services.mixins import ModelDeleteMixin, ModelUpdateMixin
from .exceptions import TaskCreateFailed, UserTasksCreateFailed, TaskAttachmentCreateFailed, TaskTreeCreateFailed, TaskDeleteRestricted
from .validators import validate_task_submission_last_date


User = get_user_model()


class TaskQuerySet(TemplateQuerySet):
    def get_task_count(self):
        return self.count()

    def get_task_status_statistics(self):
        statistics = self.values('status').annotate(count=Count('status'))
        return statistics


class Task(ModelDeleteMixin, ModelUpdateMixin, models.Model):
    restricted_fields = ['created_by', 'created_at']

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
        on_delete=models.RESTRICT,
        related_name='user_created_tasks',
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
        verbose_name=_("Task submission dadeline"),
        validators=[validate_task_submission_last_date]
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
    objects = TaskQuerySet.as_manager()

    class Meta:
        permissions = (("can_approve_disapprove_task", _("Can Approve Or Disapprove Tasks")),
                       ("can_view_all_tasks", _("Can View All Tasks")))

    def __str__(self):
        return self.title

    @classmethod
    def create_factory(cls, commit=True, **kwargs):
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
            raise TaskCreateFailed(detail=exception.__str__())
        except IntegrityError as exception:
            raise TaskCreateFailed(
                detail="Task create faield due to table data integrity error"
            )
        except TypeError as exception:
            raise TaskCreateFailed(
                detail="Table create faield due to invalid table field name"
            )

    def approve_task(self):
        if self.approval_status != self.ApprovalChoices.APPROVED:
            self.update(approval_status=self.ApprovalChoices.APPROVED)
        return True

    def reject_approval_request(self):
        if self.approval_status != self.ApprovalChoices.REJECTED:
            self.update(approval_status=self.ApprovalChoices.REJECTED)
        return True

    def accept_task_submission(self):
        if self.status == self.StatusChoices.SUBMITTED:
            return self.update(status=self.StatusChoices.COMPLETED)
        return True

    def reject_task_submission(self):
        if self.status == self.StatusChoices.SUBMITTED:
            return self.update(status=self.StatusChoices.DUE)
        return True

    def start_task(self):
        if self.status == self.StatusChoices.PENDING:
            return self.update(status=self.StatusChoices.DUE)
        return True

    def submit_task(self):
        if self.status == self.StatusChoices.DUE:
            return self.update(status=self.StatusChoices.SUBMITTED)
        return True

    def set_task_owner(self, created_by, commit=True):
        self.created_by = created_by
        if commit == True:
            self.save()
        return self

    def safe_delete(self):
        if self.approval_status == self.ApprovalChoices.APPROVED or self.status != self.StatusChoices.PENDING:
            raise TaskDeleteRestricted()
        return self.delete()

    @property
    def child_tasks(self):
        subquery = TaskTree.objects.values('child').filter(parent=self)
        sub_tasks = Task.objects.filter(pk__in=subquery)
        return sub_tasks

    @property
    def parent_tasks(self):
        try:
            parents = []
            sql = """WITH RECURSIVE parent_nodes AS (
                      SELECT parent_node.child_id, parent_node.parent_id
                      FROM task_tasktree parent_node
                      WHERE parent_node.child_id = {}
                      UNION ALL
                      SELECT parent_node.child_id, parent_node.parent_id
                      FROM task_tasktree parent_node
                      JOIN parent_nodes child_node ON child_node.parent_id = parent_node.child_id
                    )
                    SELECT parent_id
                    FROM parent_nodes;""".format(self.pk)
            with connection.cursor() as cursor:
                cursor.execute(sql)
                parents = [parent[0] for parent in cursor.fetchall()]
            return parents
        except Exception:
            return [model_to_dict(self).get('created_by')]


class UsersTasksQuerySet(TemplateQuerySet):
    def department_based_tasks(self, department_pk):
        department_members = DepartmentMember.objects.filter(department=department_pk, member=OuterRef('assigned_to'))
        members_tasks = self.filter(assigned_to=Subquery(department_members.values('member')))
        return members_tasks

    def filter_with_related_fields(self, request):
        #TODO: Update name to filter with foreignkey field
        #Default filter
        filtered_tasks = self.filter_from_query_params(request=request)
        #Filter for foreignkey relation
        for field in get_model_foreignkey_fields(self.model):
            FieldModel = field.remote_field.model
            field_name = field.name
            filtered_tasks = self.select_related(field_name).filter_from_query_params(
                request=request,
                FieldModel=FieldModel,
                related_field=field_name
            )
        return filtered_tasks


class UsersTasks(ModelDeleteMixin, ModelUpdateMixin, models.Model):
    restricted_fields = ['task']

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
    objects = UsersTasksQuerySet.as_manager()

    class Meta:
        permissions = (("can_view_inter_department_task", _("Can View Inter Department Tasks")),
                       ("can_view_all_users_tasks", _("Can View All Users Tasks")))

    def clean(self):
        task_owner_pk = model_to_dict(self.task.created_by).get('id')
        department_members = DepartmentMember.objects.filter(member__in=[task_owner_pk, self.assigned_to.pk])
        if not department_members.is_members_department_same():
            raise ValidationError("Task assignee and assignor department is not same.")

    @classmethod
    def create_factory(cls, commit=True, **kwargs):
        try:
            assert kwargs.get("task") != None, "Task should not be empty"
            assert kwargs.get("assigned_to") != None, "Task assigned_to field should not be empty"
            user_task = cls(**kwargs)
            if commit == True:
                user_task.save()
            return user_task
        except AssertionError as exception:
            raise UserTasksCreateFailed(detail=exception.__str__())
        except IntegrityError as exception:
            raise TaskCreateFailed(
                detail="user tasks create faield due to table data integrity error"
            )
        except TypeError as exception:
            raise TaskCreateFailed(
                detail="user tasks create faield due to invalid table field name"
            )


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


class TaskAttachmentsQuerySet(TemplateQuerySet):
    pass


class TaskAttachments(ModelDeleteMixin, models.Model):
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
    def create_factory(cls, commit=True, **kwargs):
        try:
            assert kwargs.get("task") != None, "Task should not be empty"
            assert kwargs.get("attachment") != None, "Attachment should not be empty"
            assert isinstance(kwargs.get("attached_by"), User), "Please provide a valid user"
            task_attachment = cls(**kwargs)
            if commit == True:
                task_attachment.save()
            return task_attachment
        except AssertionError as exception:
            raise TaskAttachmentCreateFailed(detail=exception.__str__())
        except IntegrityError as exception:
            raise TaskAttachmentCreateFailed(
                detail="task attachment create faield due to table data integrity error"
            )
        except TypeError as exception:
            raise TaskAttachmentCreateFailed(
                detail="task attachment create faield due to invalid table field name"
            )


class TaskTreeQuerySet(TemplateQuerySet):
    pass


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

    def clean(self):
        #TODO: Add department_task type, project_task type, team_task type
        if self.parent == self.child:
            raise ValidationError("Parent task and child task can not be equal")
        if self.parent.task_type == Task.TaskType.USER_TASK:
            assigned_to = UsersTasks.objects.values_list('assigned_to', flat=True).get(task=self.parent)
            if assigned_to != self.child.created_by.pk:
                raise ValidationError("Parent task assignee did not match child task owner")
        return True


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
            raise TaskTreeCreateFailed(detail=exception.__str__())
        except IntegrityError as exception:
            raise TaskTreeCreateFailed(
                detail="task tree create faield due to table data integrity error"
            )
        except TypeError as exception:
            raise TaskTreeCreateFailed(
                detail="task tree create faield due to invalid table field name"
            )



