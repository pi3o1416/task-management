
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from operator import __and__

from services.querysets import TemplateQuerySet


class DepartmentQuerySet(TemplateQuerySet):
    pass


class DesignationQuerySet(TemplateQuerySet):
    def get_department_designations(self, department_pk=None):
        return self.filter(Q(department=department_pk))


class DepartmentMemberQuerySet(TemplateQuerySet):
    def get_members_of_department(self, department_pk):
        return self.filter(Q(department=department_pk))

    def is_members_department_same(self):
        department_count = self.values('department').distinct().count()
        if department_count == 1:
            return True
        return False













