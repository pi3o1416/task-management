
from django.utils.translation import gettext_lazy as _
from django.db.models import QuerySet
from .exceptions import DepartmentGetException


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
    pass


class DepartmentMemberQuerySet(QuerySet):
    pass
