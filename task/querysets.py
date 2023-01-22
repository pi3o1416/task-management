
from functools import reduce
from operator import __and__
from django.utils.translation import gettext_lazy as _
from django.db.models import QuerySet, CharField, Q
from rest_framework.request import Request
from rest_framework.exceptions import APIException, NotFound


class TaskQuerySet(QuerySet):
    def filter_from_query_params(self, request: Request):
        try:
            q_objects = _generate_q_objects_from_query_params(self.model, request)
            if q_objects:
                return self.filter(reduce(__and__, q_objects))
            return self.all()
        except Exception as exception:
            raise APIException(detail={"detail": exception.args})

    def get_task_by_pk(self, pk):
        try:
            task = self.get(pk=pk)
            return task
        except self.model.DoesNotExist:
            raise NotFound(detail={"detail": _("Task with pk={} does not exist.".format(pk))})
        except ValueError:
            raise NotFound(detail={"detail": _("Task pk should be an integer")})
        except Exception as exception:
            raise NotFound(detail={"detail": exception.__str__()})


class TaskAttachmentsQuerySet(QuerySet):
    pass


class UsersTasksQuerySet(QuerySet):
    pass


class TaskTreeQuerySet(QuerySet):
    pass


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


