
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from department.models import Department
from department.models import DepartmentMember
from ..querysets import TeamQuerySet

User = get_user_model()

class Team(models.Model):
    title = models.CharField(
        verbose_name=_("Team title"),
        max_length=500,
    )
    description = models.TextField(
        verbose_name=_("Team description"),
    )
    department = models.ForeignKey(
        to=Department,
        on_delete=models.CASCADE,
        related_name='department_teams',
    )
    team_lead = models.ForeignKey(
        to=DepartmentMember,
        on_delete=models.SET_NULL,
        related_name='leading_teams',
        null=True,
        blank=True,
    )
    team_lead_username = models.CharField(
        verbose_name=_("Team Lead Username"),
        max_length=200,
        null=True,
        blank=True
    )
    team_lead_first_name = models.CharField(
        verbose_name=_("Team Lead First Name"),
        max_length=200,
        null=True,
        blank=True
    )
    team_lead_last_name = models.CharField(
        verbose_name=_("Team Lead Last Name"),
        max_length=200,
        null=True,
        blank=True
    )
    objects = TeamQuerySet.as_manager()

    class Meta:
        unique_together = [['department', 'title']]

    def clean(self):
        team_department = self.department
        team_lead_department = self.team_lead.department
        if team_department != team_lead_department:
            raise ValidationError(message=_("Team lead should be in same department as team"))








