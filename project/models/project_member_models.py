
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from services.exceptions import DBOperationFailed, InvalidRequest
from .project_models import Project

User = get_user_model()


class ProjectMember(models.Model):
    error_messages = {
        "CREATE": "Project member create failed.",
        "UPDATE": "Project member update failed.",
        "DELETE": "Project member delete failed.",
        "RETRIEVE": "Project member retrieve failed.",
        "PATCH": "Project member patch failed.",
    }

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
    class Meta:
        unique_together = [("project", "member")]

    @classmethod
    def create_factory(cls, commit=True, **kwargs):
        try:
            project_member = cls(**kwargs)
            if commit == True:
                project_member.save()
            return project_member
        except IntegrityError:
            raise DBOperationFailed(detail=_(cls.error_messages["CREATE"] + "Project Member already exist on this project"))
        except Exception as exception:
            raise InvalidRequest(detail=_(cls.error_messages["CREATE"] + exception.__str__()))

    def delete(self):
        try:
            super().delete()
            return True
        except Exception as exception:
            raise DBOperationFailed(detail={"detail": _(self.error_messages["DELETE"] + exception.__str__())})



class ProjectMemberSchemaLessData(models.Model):
    error_messages = {
        "CREATE": "Project member schemaless data create failed.",
        "UPDATE": "Project member schemaless data update failed.",
        "DELETE": "Project member schemaless data delete failed.",
        "RETRIEVE": "Project member schemaless data retrieve failed.",
        "PATCH": "Project member schemaless data patch failed.",
    }

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

    @classmethod
    def create_factory(cls, commit=True, **kwargs):
        try:
            project_member_schemaless_data = cls(**kwargs)
            if commit == True:
                project_member_schemaless_data.save()
            return project_member_schemaless_data
        except Exception as exception:
            raise InvalidRequest(detail=_(cls.error_messages["CREATE"] + exception.__str__()))












