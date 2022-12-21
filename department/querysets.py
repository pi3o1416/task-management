
from django.utils.translation import gettext_lazy as _
from django.db.models import QuerySet, Q
from rest_framework.exceptions import NotFound
from .exceptions import DepartmentGetException, DesignationGetException, DepartmentMemberGetException


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
    not_found_error_message = "Department member with pk={} not found"
    value_error_message = "pk should be an int"
    def get_member(self, pk):
        try:
            department_member = self.get(pk=pk)
            return department_member
        except self.model.DoesNotExist:
            message = self.not_found_error_message.format(pk)
            raise NotFound({"detail": [message]})
        except ValueError:
            raise NotFound({"detail": [self.value_error_message]})
        except Exception as exception:
            raise NotFound({"detail": exception.args})







