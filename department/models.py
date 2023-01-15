
from django.db.models import Q, UniqueConstraint
from django.db import models
from django.db.models.deletion import RestrictedError
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from .querysets import DepartmentMemberQuerySet, DepartmentQuerySet, DesignationQuerySet
from .exceptions import RestrictedDeletionError

User = get_user_model()


class Department(models.Model):
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
        return super().save(*args, **kwargs)

    def update(self, **kwargs):
        self._validate_field_names(kwargs.keys())
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def _validate_field_names(self, names):
        read_only_fields = ['pk', 'slug', 'id']
        fields = [field.name for field in self._meta.fields if field.name not in read_only_fields]
        for name in names:
            if name not in fields:
                raise KeyError("{} is not an valid field".format(name))
        return True


class Designations(models.Model):
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

    def update(self, **kwargs):
        self._validate_field_names(kwargs.keys())
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def _validate_field_names(self, names):
        read_only_fields = ['id', 'pk']
        fields = [field.name for field in self._meta.fields if field.name not in read_only_fields]
        for name in names:
            if name not in fields:
                raise KeyError("{} is not an valid field".format(name))
        return True

    def delete(self):
        try:
            super().delete()
        except RestrictedError as exception:
            raise RestrictedDeletionError({"detail": (_("Designation Delete failed due to database foreign key restriction"),)})


class DepartmentMember(models.Model):
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
    member_full_name = models.CharField(
        verbose_name=_("Department Member Full name"),
        max_length=200,
        null=True,
        blank=True,
        default=None
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

    errors = {
        "DEPARTMENT_MISMATCH": "Member department and department designation did not match.",
        "MULTIPLE_DEPARTMENT_HEAD": "Department Head of this department already exist"
    }
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
            raise ValidationError({"detail": [""]})















