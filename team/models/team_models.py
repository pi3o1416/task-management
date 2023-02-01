
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from department.models import Department
from services.exceptions import DBOperationFailed, InvalidRequest
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
        to=User,
        on_delete=models.SET_NULL,
        related_name='leading_teams',
        null=True,
        blank=True,
    )
    team_lead_full_name = models.CharField(
        verbose_name=_("Team Lead Username"),
        max_length=200,
        null=True,
        blank=True
    )
    team_lead_username = models.CharField(
        verbose_name=_("Team Lead Username"),
        max_length=200,
        null=True,
        blank=True
    )
    objects = TeamQuerySet.as_manager()

    class Meta:
        unique_together = [['department', 'title']]

    def __str__(self):
        return '{}-({})'.format(self.title, self.department)

    def clean(self):
        try:
            team_department = self.department
            team_lead_department = self.team_lead.user_department.department
            if team_department != team_lead_department:
                raise ValidationError(message=_("Team lead should be in same department as team"))
        except ValidationError as exception:
            raise ValidationError(message=_(exception.__str__()))
        except ObjectDoesNotExist as exception:
            raise ValidationError(message=_("Team lead is not assigned to any department"))

    def delete(self):
        try:
            super().delete()
            return True
        except Exception as exception:
            raise DBOperationFailed(detail={"detail":_(exception.__str__())})

    def update(self, **kwargs):
        valid_fields_for_update = ['title', 'description', 'team_lead']
        for key, value in kwargs.items():
            if key not in valid_fields_for_update:
                raise InvalidRequest(detail={"detail": _("{} is not a valid field of team model for update".format(self.pk))})
            setattr(self, key, value)
        self.save(update_fields=kwargs.keys())

    @classmethod
    def create_factory(cls, commit=False, **kwargs):
        try:
            team_instance = cls(**kwargs)
            if commit == True:
                team_instance.save()
            return team_instance
        except Exception as exception:
            raise DBOperationFailed(detail={"detail":_(exception.__str__())})









