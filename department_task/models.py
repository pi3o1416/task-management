
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models

from services.querysets import TemplateQuerySet
from department.models import Department
from task.models import Task
from .exceptions import DepartmentTaskCreateFailed


User = get_user_model()


class DepartmentTaskQuerySet(TemplateQuerySet):
    pass


class DepartmentTask(models.Model):
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
    class Meta:
        permissions = (('can_create_department_task', _("Can Create Department Task")),
                       ('can_manage_departmnet_task', _("Can Manage Department Task")))

    def clean(self):
        #Validate user has permission to create department task
        user = self.task.created_by
        if not user.has_perm('department_task.can_create_department_task'):
            raise ValidationError("Task assignor does not have permission to create department task")
        #Validate task status should be pending before assignment
        if not self.task.status == Task.StatusChoices.PENDING:
            raise ValidationError("Task status should be pending before assignment")

    @classmethod
    def create_factory(cls, commit=True, **kwargs):
        try:
            assert kwargs.get('task') != None, "Task should not be empty"
            assert kwargs.get('department') != None, "Department should not be empty"
            department_task = cls(**kwargs)
            if commit == True:
                department_task.save()
            return department_task
        except AssertionError as exception:
            raise DepartmentTaskCreateFailed(detail=exception.__str__())
        except TypeError as exception:
            raise DepartmentTaskCreateFailed(
                detail="Department task create failed due to invalid field name"
            )




