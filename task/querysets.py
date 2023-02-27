
from functools import reduce
from operator import __and__
from django.db.models import CharField, Q, TextField, Count
from django.utils.translation import gettext_lazy as _
from rest_framework.request import Request

from services.querysets import TemplateQuerySet


class TaskQuerySet(TemplateQuerySet):
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


class TaskAttachmentsQuerySet(TemplateQuerySet):
    pass


class UsersTasksQuerySet(TemplateQuerySet):
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


class TaskTreeQuerySet(TemplateQuerySet):
    pass




