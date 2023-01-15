
from django.db.models import QuerySet, Q, CharField
from django.utils.translation import gettext_lazy as _
from functools import reduce
from operator import __and__
from rest_framework.request import Request
from rest_framework.exceptions import APIException, NotFound


class GoalQuerySet(QuerySet):
    def get_department_quarter_plan(self, department, year:int, quarter:str):
        assert quarter in ["1", "2", "3", "4"], "Quarter should be an integer within {1, 2, 3, 4}"
        yearly_goals = self.get_department_yearly_plan(department=department, year=year)
        quarterly_goals = yearly_goals.filter(Q(quarter=quarter))
        return quarterly_goals

    def get_department_yearly_plan(self, department, year:int):
        department_yearly_goals = self.filter(department=department, year=year)
        return department_yearly_goals

    def get_departmnet_goals(self, department):
        goals = self.filter(department=department)
        return goals

    def filter_from_query_params(self, request: Request):
        try:
            q_objects = _generate_q_objects_from_query_params(self.model, request)
            if q_objects:
                return self.filter(reduce(__and__, q_objects))
            return self.all()
        except Exception as exception:
            raise APIException(detail={"detail": exception.args})

    def get_goal_by_pk(self, pk):
        try:
            goal = self.get(pk=pk)
            return goal
        except self.model.DoesNotExist:
            raise NotFound(detail={"detail": (_("Goal with pk={} does not exist."),)})
        except ValueError:
            raise NotFound(detail={"detail": [_("Goal primary key should be an integer.")]})
        except Exception as exception:
            raise NotFound(detail={"detail": exception.args})

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


