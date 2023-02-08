
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from services.exceptions import  InvalidRequest
from department.models import Department
from ..querysets import ProjectQuerySet

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
        verbose_name=_("Project Deadline".title())
    )
    budget = models.DecimalField(
        verbose_name=_("Project Budget".title()),
        max_digits=20,
        decimal_places=10
    )
    project_manager = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name="managed_projects",
        verbose_name=_("Project Manager".title()),
        null=True,
        blank=True,
    )
    project_owner = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name="owned_projects",
        verbose_name=_("Project Owner".title()),
        null=True,
        blank=True,
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

    def __str__(self):
        return self.title

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
            raise InvalidRequest(detail={"detail":_(exception.__str__())})




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
















