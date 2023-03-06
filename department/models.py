
from django.db import models
from django.db.models import Q, UniqueConstraint
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from services.mixins import ModelDeleteMixin, ModelUpdateMixin

from .querysets import DepartmentMemberQuerySet, DepartmentQuerySet, DesignationQuerySet

User = get_user_model()


class Department(ModelDeleteMixin, ModelUpdateMixin, models.Model):
    restricted_fields = ['pk', 'slug']
    error_messages = {
        "CREATE": "Department create failed.",
        "UPDATE": "Department update failed.",
        "DELETE": "Department delete failed.",
        "RETRIEVE": "Department retrieve failed.",
        "PATCH": "Department patch failed.",
    }

    name = models.CharField(
        verbose_name=_("Department Name"),
        max_length=200,
        null=False,
        unique=True,
        blank=False,
    )
    slug = models.SlugField(
        verbose_name=_("Department Name SLug"),
        unique=True,
        null=False,
    )
    description = models.TextField(
        verbose_name=_("Department Description"),
        null=False,
        blank=False,
    )
    objects = DepartmentQuerySet.as_manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.clean()
        return super().save(*args, **kwargs)


class Designations(ModelDeleteMixin, ModelUpdateMixin, models.Model):
    restricted_fields = ['pk']
    error_messages = {
        "CREATE": "Designation create failed.",
        "UPDATE": "Designation update failed.",
        "DELETE": "Designation delete failed.",
        "RETRIEVE": "Designation retrieve failed.",
        "PATCH": "Designation patch failed.",
    }

    department = models.ForeignKey(
        to=Department,
        on_delete=models.CASCADE,
        related_name="department_designations",
        verbose_name=_("Department Designations")
    )
    title = models.CharField(
        verbose_name=_("Designation Title"),
        max_length=100,
        null=False,
        blank=False,
    )
    objects = DesignationQuerySet.as_manager()

    class Meta:
        unique_together = [['department', 'title']]


    def __str__(self):
        return '{}-{}'.format(self.department, self.title)


class DepartmentMember(ModelDeleteMixin, ModelUpdateMixin, models.Model):
    restricted_fields = ['pk', 'member', '']
    error_messages = {
        "CREATE": "Department create failed.",
        "UPDATE": "Department update failed.",
        "DELETE": "Department delete failed.",
        "RETRIEVE": "Department retrieve failed.",
        "PATCH": "Department patch failed.",
        "DEPARTMENT_MISMATCH": "Member department and department designation did not match.",
        "MULTIPLE_DEPARTMENT_HEAD": "Department Head of this department already exist"
    }

    member = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="user_department",
        null=False,
        blank=False,
        verbose_name=_("Member"),
        primary_key=True,
    )
    department = models.ForeignKey(
        to=Department,
        on_delete=models.CASCADE,
        related_name="department_members",
        null=False,
        blank=False,
        verbose_name="Department"
    )
    designation = models.ForeignKey(
        to=Designations,
        on_delete=models.RESTRICT,
        null=False,
        blank=False,
        verbose_name="designated_members"
    )
    is_head = models.BooleanField(
        verbose_name=_("Department Head"),
        default=False,
    )
    department_name = models.CharField(
        verbose_name=_("Department Name"),
        max_length=200,
        null=True,
        blank=True,
        default=None
    )
    designation_title = models.CharField(
        verbose_name=_("Designation Title"),
        max_length=100,
        null=True,
        blank=True,
        default=None
    )
    objects = DepartmentMemberQuerySet.as_manager()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["department"],
                condition=Q(is_head=True),
                name="one_head_per_department"
            )
        ]
    def __str__(self):
        return "{}".format(self.member.first_name)

    def clean(self):
        if self.department != self.designation.department:
            raise ValidationError({"detail": [self.error_messages["DEPARTMENT_MISMATCH"]]})















