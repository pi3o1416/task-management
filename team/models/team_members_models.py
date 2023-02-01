
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from services.exceptions import DBOperationFailed
from .team_models import Team
from ..querysets import TeamMemberQuerySet

User = get_user_model()


class TeamMember(models.Model):
    team = models.ForeignKey(
        to=Team,
        on_delete=models.CASCADE,
        related_name='team_members',
    )
    member = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='user_teams'
    )
    member_full_name = models.CharField(
        max_length=200,
        verbose_name=_("Member full name"),
        null=True,
        blank=True,
    )
    member_username = models.CharField(
        max_length=200,
        verbose_name=_("Member username"),
        null=True,
        blank=True,
    )
    objects = TeamMemberQuerySet.as_manager()

    class Meta:
        unique_together = [['team', 'member']]

    def delete(self):
        try:
            super().delete()
            return True
        except Exception as exception:
            raise DBOperationFailed(detail={"detail":_(exception.__str__())})

    @classmethod
    def create_factory(cls, commit=False, **kwargs):
        try:
            team_member_instance = cls(**kwargs)
            if commit == True:
                team_member_instance.save()
            return team_member_instance
        except Exception as exception:
            raise DBOperationFailed(detail={"detail":_(exception.__str__())})





