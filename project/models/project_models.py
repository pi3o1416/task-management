
import os
from django.forms.models import model_to_dict
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.conf import settings

from services.exceptions import DBOperationFailed, InvalidRequest
from department.models import Department

from ..querysets import ProjectQuerySet, ProjectAttachmentQuerySet
from ..validators import validate_project_deadline, validate_project_manager_permission, validate_project_owner_permission, validate_budget

User = get_user_model()


class Project(models.Model):
    class ProjectStatus(models.TextChoices):
        PAUSED = "PAU", _("Paused")
        ACTIVE = "ACT", _("Active")
        FINISHED = "FIN", _("Active")

    error_messages = {
        "CREATE": "Project create failed.",
        "UPDATE": "Project update failed.",
        "DELETE": "Project delete failed.",
        "RETRIEVE": "Project retrieve failed.",
        "PATCH": "Project patch failed.",
        "MEMBER_DELETE": "Project member delete failed."
    }

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
    members = models.ManyToManyField(
        to=User,
        related_name='user_projects',
        verbose_name=_("Project Members")
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
                raise ValidationError(
                    message=_(
                        self.error_messages["CREATE"] + ": Project manager should in same department as user department")
                )
        except ObjectDoesNotExist:
            raise ValidationError(
                message=_(
                    self.error_messages["CREATE"] + "Project manager does not belong to any department")
            )

    def __str__(self):
        return self.title

    def delete(self):
        try:
            super().delete()
            return True
        except Exception as exception:
            raise DBOperationFailed(detail={
                "detial": _(self.error_messages["DELETE"] + exception.__str__())
            })

    @classmethod
    def create_factory(cls, commit=True, **kwargs):
        try:
            project = cls(
                **kwargs
            )
            if commit == True:
                project.save()
            return project
        except IntegrityError as exception:
            raise DBOperationFailed(detail={
                "detail": _(cls.error_messages["CREATE"] + "Project with same title and department already exist.")
            })
        except Exception as exception:
            raise InvalidRequest(detail={
                "detail": _(cls.error_messages["CREATE"] + exception.__str__())
            })

    @property
    def extended_data(self):
        try:
            return self.schemaless_data
        except ObjectDoesNotExist:
            return None

    @property
    def project_manager_pk(self):
        return model_to_dict(self).get("project_manager")

    def update(self, commit=True, **kwargs):
        previous_state = self
        fields = [field.name for field in self._meta.fields]
        for key, value in kwargs.items():
            if key in fields:
                setattr(self, key, value)
            else:
                self = previous_state
                raise InvalidRequest(detail={
                    "detail": _("{} {} is not an valid field of Project model.".format(self.error_messages["UPDATE"], key))
                })
        if commit == True:
            if self.pk != None:
                self.save(update_fields=kwargs.keys())
            else:
                self.save()
        return True


    def active_project(self):
        if self.status != self.ProjectStatus.ACTIVE:
            self.update(status=self.ProjectStatus.ACTIVE)
        return True

    def finish_project(self):
        if self.status != self.ProjectStatus.FINISHED:
            self.update(status=self.ProjectStatus.FINISHED)
        return True

    def pause_project(self):
        if self.status != self.ProjectStatus.FINISHED:
            self.update(status=self.ProjectStatus.PAUSED)
        return True

    def get_project_members(self):
        return self.members.all()

    def get_project_attachments(self):
        return self.project_attachments.all()

    def delete_project_member(self, user):
        try:
            user_pk = user.pk
            project_manager_pk = model_to_dict(self).get('project_manager')
            if user_pk == project_manager_pk:
                raise IntegrityError(_("The user assigned as the project manager of the project"))
            self.members.remove(user)
            return True
        except IntegrityError as exception:
            raise InvalidRequest(detail={
                "detail": "{} {}".format(self.error_messages["MEMBER_DELETE"], exception.__str__())
            })


class ProjectSchemaLessData(models.Model):
    error_messages = {
        "CREATE": "Project schemaless data create failed.",
        "UPDATE": "Project schemaless data update failed.",
        "DELETE": "Project schemaless data delete failed.",
        "RETRIEVE": "Project schemaless data retrieve failed.",
        "PATCH": "Project schemaless data patch failed.",
    }

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
            raise InvalidRequest(
                detail={"detail": _(
                    cls.error_messages["CREATE"] + exception.__str__())}
            )


def project_attachment_upload_path(instance, filename):
    file_path = 'project-attachments/{}/{}'.format(
        instance.project.pk, filename)
    desired_path = os.path.join(settings.MEDIA_ROOT, file_path)
    name, extension = os.path.splitext(filename)
    counter = 1
    while os.path.exists(desired_path) == True:
        file_path = 'project-attachments/{}/{}_{}{}'.format(
            instance.project.pk, name, counter, extension)
        desired_path = os.path.join(settings.MEDIA_ROOT, file_path)
        counter += 1
    return file_path


class ProjectAttachment(models.Model):
    error_messages = {
        "CREATE": "Project attachment create failed.",
        "UPDATE": "Project attachment update failed.",
        "DELETE": "Project attachment delete failed.",
        "RETRIEVE": "Project attachment retrieve failed.",
        "PATCH": "Project attachment patch failed.",
    }

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='project_attachments',
        verbose_name=_("Project")
    )
    attached_by = models.ForeignKey(
        to=User,
        on_delete=models.RESTRICT,
        related_name='attachments_on_project',
        verbose_name=_("Attached by".title())
    )
    attachment = models.FileField(
        upload_to=project_attachment_upload_path,
        verbose_name=_("Project Attachment".title())
    )
    attached_at = models.DateTimeField(
        verbose_name=_("Attached at".title()),
        auto_now_add=True
    )
    objects = ProjectAttachmentQuerySet.as_manager()

    def clean(self):
        project = self.project
        if not project.get_project_members().filter(member=self.attached_by).exists():
            raise ValidationError(message=_(
                self.error_messages["CREATE"] + "Attached by user does not belong to this project."))

    @classmethod
    def create_factory(cls, commit=True, **kwargs):
        try:
            if commit == True:
                assert isinstance(kwargs.get("attached_by"), User), "Please provide a valid user"
                assert kwargs.get("project") != None, "Project should not be empty"
            assert kwargs.get("attachment") != None, "Attachment should not be empty"
            project_attachment = cls(**kwargs)
            if commit == True:
                project_attachment.save()
            return project_attachment
        except AssertionError as exception:
            raise InvalidRequest(detail={
                "detail": _("{} {}".format(cls.error_messages["CREATE"], exception.__str__()))
            })
        except Exception as exception:
            raise InvalidRequest(detail={
                "detail": _(cls.error_messages["CREATE"] + exception.__str__())
            })

    def delete(self):
        try:
            super().delete()
            return True
        except Exception as exception:
            raise DBOperationFailed(detail={
                "detail": _(self.error_messages["DELETE"] + exception.__str__())
            })

    def update(self, commit=True, **kwargs):
        previous_state = self
        fields = [field.name for field in self._meta.fields]
        for key, value in kwargs.items():
            if key in fields:
                setattr(self, key, value)
            else:
                self = previous_state
                raise InvalidRequest(detail={
                    "detail": _(self.error_messages["UPDATE"] + "{} is not an valid field of Project model.")
                })
        if commit == True:
            if self.pk != None:
                self.save(update_fields=kwargs.keys())
            else:
                self.save()
        return True

    @property
    def attached_by_user_username(self):
        return self.attached_by.username

    @property
    def attached_by_user_fullname(self):
        return self.attached_by.full_name
