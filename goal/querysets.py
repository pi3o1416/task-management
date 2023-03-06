
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from services.querysets import TemplateQuerySet



class GoalQuerySet(TemplateQuerySet):
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

