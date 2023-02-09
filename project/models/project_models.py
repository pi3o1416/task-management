
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from services.exceptions import  DBOperationFailed, InvalidRequest
from department.models import Department
from ..querysets import ProjectQuerySet
from ..validators import validate_project_deadline, validate_project_manager_permission, validate_project_owner_permission, validate_budget

User = get_user_model()


class Project(models.Model):
    class ProjectStatus(models.TextChoices):
        PAUSED = "PAU", _("Paused")
        ACTIVE = "ACT", _("Active")
        FINISHED = "FIN", _("Active")

    title = models.CharField(
        verbose_name=_("Project Title".title()),
        max_length=500
    )
    description = models.TextField(
        verbose_name=_("Project Description".title())
    )
    deadline = models.DateField(
        verbose_name=_("Project Deadline".title()),
        validators=[validate_project_deadline]
    )
    budget = models.DecimalField(
        verbose_name=_("Project Budget".title()),
        max_digits=20,
        decimal_places=10,
        validators=[validate_budget],
    )
    project_manager = models.ForeignKey(
        to=User,
        on_delete=models.RESTRICT,
        related_name="managed_projects",
        verbose_name=_("Project Manager".title()),
        validators=[validate_project_manager_permission]
    )
    project_owner = models.ForeignKey(
        to=User,
        on_delete=models.RESTRICT,
        related_name="owned_projects",
        verbose_name=_("Project Owner".title()),
        validators=[validate_project_owner_permission]
    )
    department = models.ForeignKey(
        to=Department,
        related_name="department_projects",
        on_delete=models.CASCADE,
        verbose_name=_("Department Projects".title())
    )
    status = models.CharField(
        verbose_name=_("Project Status".title()),
        max_length=3,
        choices=ProjectStatus.choices,
        default=ProjectStatus.PAUSED,
    )
    objects = ProjectQuerySet.as_manager()

    class Meta:
        unique_together = [['department', 'title']]
        permissions = (("can_maintain_project", _("Can manage a project".title())),
                       ("can_own_project", _("Can own project".title())),
                       ("can_view_all_project", _("Can View All Projects".title())))

    def clean(self):
        try:
            project_manager = self.project_manager
            if project_manager.user_department.department != self.department:
                raise ValidationError(message=_("Project manager should in same department as user department"))
        except ObjectDoesNotExist:
            raise ValidationError(message=_("Project manager does not belong to any department"))

    def __str__(self):
        return self.title

    def delete(self):
        try:
            super().delete()
            return True
        except Exception as exception:
            raise DBOperationFailed(detail={"detial":_(exception.__str__())})

    @classmethod
    def create_factory(cls, commit=True, **kwargs):
        try:
            project = cls(
                **kwargs
            )
            if commit == True:
                project.save()
            return project
        except Exception as exception:
            raise InvalidRequest(detail={"detail": _(exception.__str__())})

    @property
    def extended_data(self):
        try:
            return self.schemaless_data
        except ObjectDoesNotExist:
            return None

    @classmethod
    def update(cls, instance_pk, **kwargs):
        try:
            instance = cls(pk=instance_pk, **kwargs)
            instance.save(update_fields=kwargs.keys())
            return instance
        except Exception as exception:
            raise InvalidRequest(detail={"detail": _(exception.__str__())})

class ProjectSchemaLessData(models.Model):
    project = models.OneToOneField(
        to=Project,
        on_delete=models.CASCADE,
        related_name='schemaless_data',
        verbose_name=_("Schemaless Data".title())
    )
    department_title = models.CharField(
        verbose_name=_("Department Title".title()),
        max_length=200
    )
    project_owner_fullname = models.CharField(
        verbose_name=_("Project Owner Fullname".title()),
        max_length=200,
    )
    project_owner_username = models.CharField(
        verbose_name=_("Project Owner Username".title()),
        max_length=200,
    )
    project_manager_fullname = models.CharField(
        verbose_name=_("Project Manager Fullname".title()),
        max_length=200,
    )
    project_manager_username = models.CharField(
        verbose_name=_("Project Manager Username".title()),
        max_length=200,
    )

    @classmethod
    def create_factory(cls, commit=True, **kwargs):
        try:
            project_schemaless_data = cls(
                **kwargs
            )
            if commit == True:
                project_schemaless_data.save()
            return project_schemaless_data
        except Exception as exception:
            raise InvalidRequest(detail={"detail":_(exception.__str__())})
















