
from django.utils.translation import gettext_lazy as _
from django.db.models import QuerySet, Q
from .exceptions import DepartmentGetException, DesignationGetException


class DepartmentQuerySet(QuerySet):
    def get_department(self, pk):
        try:
            department = self.get(pk=pk)
            return department
        except self.model.DoesNotExist:
            raise DepartmentGetException(_("Department with pk={} does not exist".format(pk)))
        except ValueError:
            raise DepartmentGetException(_("Department pk should be an integer"))
        except Exception as exception:
            raise DepartmentGetException(*exception.args)


class DesignationQuerySet(QuerySet):
    def get_designation(self, pk):
        try:
            designation = self.get(pk=pk)
            return designation
        except self.model.DoesNotExist:
            raise DesignationGetException(_("Designation with pk={} does not exist".format(pk)))
        except ValueError:
            raise DesignationGetException(_("Designation pk should be an integer"))
        except Exception as exception:
            raise DesignationGetException(*exception.args)

    def get_department_designations(self, department_pk=None):
        return self.filter(Q(department=department_pk))


class DepartmentMemberQuerySet(QuerySet):
    pass
