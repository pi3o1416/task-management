
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
from .querysets import DepartmentMemberQuerySet, DepartmentQuerySet, DesignationQuerySet

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


class DepartmentMember(models.Model):
    Member = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="user_departments",
        null=False,
        blank=False,
        verbose_name=_("Member")
    )
    department = models.ForeignKey(
        to=Department,
        on_delete=models.CASCADE,
        related_name="department_members",
        null=False,
        blank=False,
        verbose_name="Department"
    )
    Designation = models.ForeignKey(
        to=Designations,
        on_delete=models.RESTRICT,
        null=False,
        blank=False,
        verbose_name="designated_member"
    )
    objects = DepartmentMemberQuerySet.as_manager()













