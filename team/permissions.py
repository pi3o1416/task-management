
from django.forms import model_to_dict
from rest_framework.permissions import BasePermission

from department.models import DepartmentMember
from services.decorators import has_kperms, is_authenticated


@has_kperms(perms=['team.add_team'])
class CanCreateTeam(BasePermission):
    pass


@has_kperms(perms=['team.can_view_all_teams'])
class CanViewAllTeams(BasePermission):
    pass


@has_kperms(perms=['team.delete_team'])
class CanDeleteTeam(BasePermission):
    pass


@has_kperms(perms=['team.change_team'])
class CanChangeTeam(BasePermission):
    pass


class IsTeamLeadOfTeam(BasePermission):
    @is_authenticated
    def has_object_permission(self, request, view, team):
        team_lead = model_to_dict(team, fields=['team_lead']).get('team_lead')
        if request.user.pk == team_lead:
            return True
        return False






class IsTeamAndUserDepartmentSame(BasePermission):

    @is_authenticated
    def has_object_permission(self, request, view, team):
        team_department = model_to_dict(team, fields=['department']).get('department')
        user_department = DepartmentMember.objects.member_department(member_pk=request.user.pk)
        if team_department == user_department:
            return True
        return False
