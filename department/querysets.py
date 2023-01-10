
from operator import __and__
from functools import reduce
from django.utils.translation import gettext_lazy as _
from django.db.models import QuerySet, Q, CharField
from rest_framework.exceptions import NotFound, APIException
from rest_framework.request import Request


class DepartmentQuerySet(QuerySet):
    def get_department(self, pk):
        try:
            department = self.get(pk=pk)
            return department
        except self.model.DoesNotExist:
            raise NotFound({"detail": [_("Department with pk={} does not exist".format(pk))]})
        except ValueError:
            raise NotFound({"detail": [_("Department pk should be an integer")]})
        except Exception as exception:
            raise NotFound({"detail": exception.args})


class DesignationQuerySet(QuerySet):
    def get_designation(self, pk):
        try:
            designation = self.get(pk=pk)
            return designation
        except self.model.DoesNotExist:
            raise NotFound({"detail": [_("Designation with pk={} does not exist".format(pk))]})
        except ValueError:
            raise NotFound({"detail": [_("Designation pk should be an integer")]})
        except Exception as exception:
            raise NotFound({"detail": exception.args})

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

    def get_members_of_department(self, department_pk):
        return self.filter(Q(department=department_pk))

    def filter_from_query_prams(self, request: Request):
        try:
            q_objects = _generate_q_objects_from_query_params(self.model, request)
            if q_objects:
                return self.filter(reduce(__and__, q_objects))
            return self.all()
        except Exception as exception:
            raise APIException(detail={"detail": exception.args})

    def is_department_head_exist(self, department):
        return self.filter(Q(department=department), Q(is_head=True)).exists()

def _generate_q_objects_from_query_params(Model, request: Request) -> list:
    query_params = request.query_params
    fields = {field.name: field for field in Model._meta.fields}
    q_objects = []
    for param, value in query_params.items():
        if param in fields.keys():
            if isinstance(fields[param], CharField):
                q_objects.append(Q(('{}__icontains'.format(param), value)))
            else:
                q_objects.append(Q((param, value)))
    return q_objects














