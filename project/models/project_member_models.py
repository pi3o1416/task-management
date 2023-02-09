
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models

from .project_models import Project

User = get_user_model()


class ProjectMember(models.Model):
    project = models.ForeignKey(
        to=Project,
        related_name='project_members',
        on_delete=models.CASCADE,
        verbose_name=_("Project")
    )
    member = models.ForeignKey(
        to=User,
        on_delete=models.RESTRICT,
        related_name='user_projects',
        verbose_name=_("Project Member")
    )


class ProjectMemberSchemaLessData(models.Model):
    project = models.OneToOneField(
        to=ProjectMember,
        on_delete=models.CASCADE,
        related_name='project_member_schemaless_data',
        verbose_name=_("Project")
    )
    project_title = models.CharField(
        max_length=500,
        verbose_name=_("Project Title"),
    )
    member_username = models.CharField(
        max_length=200,
        verbose_name=_("Member Username")
    )
    member_fullname = models.CharField(
        max_length=200,
        verbose_name=_("Member Fullname")
    )












