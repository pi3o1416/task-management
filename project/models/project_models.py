
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from department.models import Department

User = get_user_model()


class Project(models.Model):
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

    def __str__(self):
        return self.title













