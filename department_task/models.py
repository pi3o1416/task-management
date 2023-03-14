
from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from django.utils.translation import gettext_lazy as _
from django.db import models
from rest_framework.exceptions import ValidationError

from services.mixins import ModelUpdateMixin, ModelDeleteMixin
from services.querysets import TemplateQuerySet
from department.models import Department
from task.models import Task
from .exceptions import DepartmentTaskCreateFailed


User = get_user_model()


class DepartmentTaskQuerySet(TemplateQuerySet):
    def user_department_tasks(self, user):
        return self.select_related('task').filter(
            task__created_by=user,
            task__task_type=Task.TaskType.DEPARTMENT_TASK
        )


class DepartmentTask(ModelUpdateMixin, ModelDeleteMixin, models.Model):
    restricted_fields = ['task', 'pk']

    task = models.OneToOneField(
        to=Task,
        on_delete=models.CASCADE,
        related_name="assigned_to_dept",
        verbose_name=_("Task")
    )
    department = models.ForeignKey(
        to=Department,
        on_delete=models.CASCADE,
        related_name='department_tasks',
        verbose_name=_("Department"),
    )
    objects = DepartmentTaskQuerySet.as_manager()
    class Meta:
        permissions = (('can_manage_departmnet_task', _("Can Manage Department Task")),)

    def clean(self):
        user = self.task.created_by
        #Validate user has permission to create department task
        if not user.has_perm('department_task.add_departmenttask'):
            raise ValidationError("Task assignor does not have permission to create department task")
        #Validate task status should be pending before assignment
        if not self.task.status == Task.StatusChoices.PENDING:
            raise ValidationError("Task status should be pending before assignment")
        #Validate task type should be none before assignment
        if not self.task.pk and not self.task.task_type == Task.TaskType.NONE:
            raise ValidationError("Task type should be none before assignment")
        #Validate user can not assign task to own department
        if model_to_dict(user.user_department).get('department') == self.department.pk:
            raise ValidationError("Department member can not assign task to his own department")


    @classmethod
    def create_factory(cls, task, department, commit=True):
        try:
            department_task = cls(
                task=task,
                department=department
            )
            if commit == True:
                department_task.save()
            return department_task
        except AssertionError as exception:
            raise DepartmentTaskCreateFailed(detail=exception.__str__())
        except TypeError as exception:
            raise DepartmentTaskCreateFailed(
                detail="Department task create failed due to invalid field name"
            )




