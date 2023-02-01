
from operator import __and__
from functools import reduce
from django.utils.translation import gettext_lazy as _
from django.db.models import CharField, Q, QuerySet
from rest_framework.request import Request
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound


class TemplateQuerySet(QuerySet):
    def get_object_by_pk(self, pk):
        try:
            obj = self.get(pk=pk)
            return obj
        except self.model.DoesNotExist:
            raise NotFound(detail={"detail": _("Ojbect with pk={} does not exist".format(pk))})
        except ValueError as exception:
            raise NotFound(detail={"detail": _("Object primary key shoud be integer")})
        except Exception as exception:
            raise NotFound(detail={"detail": _(exception.__str__())})

    def filter_from_query_params(self, request: Request):
       try:
           q_objects = generate_q_objects_from_query_params(self.model, request)
           if q_objects:
               return self.filter(reduce(__and__, q_objects))
           return self.all()
       except Exception as exception:
           raise APIException(detail={"detail": exception.args})


def generate_q_objects_from_query_params(Model, request: Request) -> list:
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


