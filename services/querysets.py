
from operator import __and__
from functools import reduce
from django.utils.translation import gettext_lazy as _
from django.db.models import CharField, Q, QuerySet, Model, TextField
from rest_framework.request import Request
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from .exceptions import InvalidRequest


class TemplateQuerySet(QuerySet):
    def filter_objects_by_pk(self, pks:list):
        return self.filter(pk__in=pks)

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

    def filter_from_query_params(self, request: Request, FieldModel=None, related_field=None):
        """
        Filter queryset from request query parameters.
        Parameter:
            request         : Request object
            related_field   : field_name of Foreign Key field.(None if not filter in )
            Model           : Model of related_field.(If filter in related field)
        Return:
            Filtered queryset
        """
        assert not ((related_field != None) ^ (FieldModel != None)), "If related_field is True, Provide a Model."
        try:
            if not FieldModel:
                FieldModel = self.model
            q_objects = generate_q_objects_from_query_params(FieldModel, request, related_field)
            if q_objects:
                return self.filter(reduce(__and__, q_objects))
            return self.all()
        except Exception as exception:
           raise InvalidRequest(detail={"detail": exception.args})


def generate_q_objects_from_query_params(ModelName, request: Request, related_field=None):
    query_params = request.query_params
    fields = {field.name: field for field in ModelName._meta.fields}
    q_objects = []
    for param, value in query_params.items():
        if related_field:
            parent_field, child_field = param.split('.')
            if child_field and parent_field == related_field:
                param = child_field
            else:
                continue
        if param in fields.keys():
            q_object = get_q_object(fields=fields, field=param, value=value, related_field=related_field)
            q_objects.append(q_object)
    return q_objects

def get_q_object(fields, field, value, related_field=None):
    if isinstance(fields[field], CharField) or isinstance(fields[field], TextField):
        return _get_textdata_q_object(field=field, value=value, related_field=related_field)
    else:
        return _get_default_q_object(field=field, value=value, related_field=related_field)

def _get_textdata_q_object(field, value, related_field=None):
    if related_field:
        return Q(('{}__{}__icontains'.format(related_field, field), value))
    return Q(('{}__icontains'.format(field), value))

def _get_default_q_object(field, value, related_field=None):
    if related_field:
        return Q(('{}__{}'.format(related_field, field), value))
    return Q((field, value))

def get_model_foreignkey_fields(ModelName):
    for field in ModelName._meta.fields:
        if field.remote_field:
            yield field





