
from operator import __and__
from django.db.models import QuerySet, Q


class GoalQuerySet(QuerySet):
    def get_department_quarter_plan(self, department, year:int, quarter:int):
        assert quarter in [1, 2, 3, 4], "Quarter should be an integer within {1, 2, 3, 4}"
        yearly_goals = self.get_department_yearly_plan(department=department, year=year)
        quarters = {
            1: self.model.QuarterChoices.QUARTER1,
            2: self.model.QuarterChoices.QUARTER2,
            3: self.model.QuarterChoices.QUARTER3,
            4: self.model.QuarterChoices.QUARTER4
        }
        quarterly_goals = yearly_goals.filter(Q(quarter=quarters[quarter]))
        return quarterly_goals

    def get_department_yearly_plan(self, department, year:int):
        department_yearly_goals = self.filter(department=department, year=year)
        return department_yearly_goals


