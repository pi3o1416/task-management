
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from department.models import Department, DepartmentMember
from services.exceptions import ModelCleanValidationFailed
from services.mixins import ModelUpdateMixin, ModelDeleteMixin
from ..querysets import TeamQuerySet
from ..exceptions import TeamCreateFailed

User = get_user_model()

class Team(ModelDeleteMixin, ModelUpdateMixin, models.Model):
    restricted_fields = ['pk', 'department']
    CACHED_FIELDS = ['pk', 'title', 'description', 'department', 'team_lead']

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
        to=User,
        on_delete=models.RESTRICT,
        related_name='leading_teams',
    )
    members = models.ManyToManyField(
        to=User,
        related_name='teams',
        verbose_name=_("Members")
    )
    objects = TeamQuerySet.as_manager()

    class Meta:
        unique_together = [['department', 'title']]
        permissions = (("can_view_all_teams", _("Can View All Teams")),)

    def __str__(self):
        return '{}-({})'.format(self.title, self.department)

    def clean(self, **kwargs):
        #Validate team lead department and team department should be equal
        team_lead_department_pk = DepartmentMember.objects.member_department(member_pk=self.team_lead_id)
        if team_lead_department_pk != self.department_id:
            raise ModelCleanValidationFailed(detail=_("Team department and Team Lead department should be same"))

    def save(self, **kwargs):
        self.clean(**kwargs)
        return super().save(**kwargs)

    @classmethod
    def create_factory(cls, commit=False, **kwargs):
        try:
            team_instance = cls(**kwargs)
            if commit == True:
                team_instance.save()
            return team_instance
        except Exception as exception:
            raise TeamCreateFailed(detail=_(exception.__str__()))









