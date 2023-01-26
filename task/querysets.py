
from functools import reduce
from operator import __and__
from django.utils.translation import gettext_lazy as _
from django.db.models import QuerySet, CharField, Q, TextField, Count
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

    def get_subtasks(self, parent_task):
        subtasks = self.filter(task_parent__parent=parent_task)
        return subtasks

    def get_subtask_count(self, parent_task):
        subtasks = self.get_subtasks(parent_task=parent_task)
        return subtasks.count()

    def get_task_count(self):
        return self.count()

    def get_subtasks_statistics(self, parent_task):
        subtasks = self.get_subtasks(parent_task=parent_task)
        subtasks_statistics = subtasks.get_task_status_statistics()
        return subtasks_statistics

    def get_task_status_statistics(self):
        statistics = self.values('status').annotate(count=Count('status'))
        return statistics


class TaskAttachmentsQuerySet(QuerySet):
    def get_attachment_by_pk(self, pk):
        try:
            attachment = self.get(pk=pk)
            return attachment
        except self.model.DoesNotExist:
            raise NotFound(detail={"detail": _("Attachment with pk={} does not exist.".format(pk))})
        except ValueError:
            raise NotFound(detail={"detail": _("Attachment pk should be an integer")})
        except Exception as exception:
            raise NotFound(detail={"detail": exception.__str__()})


class UsersTasksQuerySet(QuerySet):
    def filter_from_query_params(self, request: Request):
       try:
           q_objects = _generate_q_objects_from_query_params(self.model, request)
           if q_objects:
               return self.filter(reduce(__and__, q_objects))
           return self.all()
       except Exception as exception:
           raise APIException(detail={"detail": exception.args})

    def filter_with_task(self, request: Request):
        query_params = request.query_params
        task_model = self.model._meta.get_field('task').remote_field.model
        fields = {field.name: field for field in task_model._meta.fields}
        q_objects = []
        for param, value in query_params.items():
            if param in fields.keys():
                if isinstance(fields[param], CharField) or isinstance(fields[param], TextField):
                    q_objects.append(Q(('task__{}__icontains'.format(param), value)))
        return self.filter_with_q_objects(q_objects=q_objects)

    def filter_with_q_objects(self, q_objects):
        try:
            if q_objects:
                return self.filter(reduce(__and__, q_objects))
            return self.all()
        except Exception as exception:
            raise APIException(detail={"detail": exception.__str__()})

    def get_user_task_by_pk(self, pk):
        try:
            user_task = self.get(pk=pk)
            return user_task
        except self.model.DoesNotExist:
            raise NotFound(detail={"detail": _("User task with pk={} does not exist.".format(pk))})
        except ValueError:
            raise NotFound(detail={"detail": _("Task pk should be an integer")})
        except Exception as exception:
            raise NotFound(detail={"detail": exception.__str__()})


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


