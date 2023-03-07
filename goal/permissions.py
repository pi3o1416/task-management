
from django.forms import model_to_dict
from rest_framework.permissions import BasePermission

from department.models import DepartmentMember
from services.decorators import has_kperms, is_authenticated


@has_kperms(['goal.view_goal'])
class CanViewGoal(BasePermission):
    pass


@has_kperms(['goal.add_goal'])
class CanCreateGoal(BasePermission):
    pass


@has_kperms(['goal.can_view_all_goals'])
class CanViewAllGoals(BasePermission):
    pass


@has_kperms(['goal.change_goal'])
class CanChangeGoal(BasePermission):
    pass


@has_kperms(['goal.delete_goal'])
class CanDeleteGoal(BasePermission):
    pass


@has_kperms(['goal.can_change_status'])
class CanChangeGoalStatus(BasePermission):
    pass


@has_kperms(['review.add_review'])
class CanAddReview(BasePermission):
    pass


class IsGoalAndUserDepartmentSame(BasePermission):
    @is_authenticated
    def has_object_permission(self, request, view, goal):
        user = request.user
        user_department_pk = DepartmentMember.objects.member_department(member=user)
        goal_department_pk = model_to_dict(goal).get('department')
        if user_department_pk != goal_department_pk:
            return False
        return True



