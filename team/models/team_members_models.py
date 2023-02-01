
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .team_models import Team

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







