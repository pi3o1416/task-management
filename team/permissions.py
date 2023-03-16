
from rest_framework.permissions import BasePermission

from project.models import ProjectTask
from department.models import DepartmentMember
from department_task.models import DepartmentTask
from task.models import Task
from department.models import DepartmentMember
from services.decorators import has_kperms, is_authenticated


@has_kperms(perms=['team.add_teamtasks'])
class CanCreateTeamTasks(BasePermission):
    message = "You do not have permission to create team task"


@has_kperms(perms=['team.can_manage_team_tasks'])
class CanManageTeamTasks(BasePermission):
    message = "You do not have permission to manage team tasks"


@has_kperms(perms=['team.add_team'])
class CanCreateTeam(BasePermission):
    message = "You do not have permission to create team task"


@has_kperms(perms=['team.can_view_all_teams'])
class CanViewAllTeams(BasePermission):
    message = "You do not have permission to view all team tasks"


@has_kperms(perms=['team.delete_team'])
class CanDeleteTeam(BasePermission):
    message = "You do not have permission to delete team task"


@has_kperms(perms=['team.change_team'])
class CanChangeTeam(BasePermission):
    message = "You do not have permission to change team instance"


class IsMemberOfTeam(BasePermission):
    message = "You are not a member of this team"
    @is_authenticated
    def has_object_permission(self, request, view, team):
        user_pk = request.user.pk
        if team.members.filter(pk=user_pk).exists():
            return True
        return False


class IsTeamLeadOfTeam(BasePermission):
    message = "You are not the team lead of this team"
    @is_authenticated
    def has_object_permission(self, request, view, team):
        if request.user.pk == team.team_lead_id:
            return True
        return False


class IsTeamAndUserDepartmentSame(BasePermission):
    message = "Team Department and your department do not match"
    @is_authenticated
    def has_object_permission(self, request, view, team):
        user_department = DepartmentMember.objects.member_department(member_pk=request.user.pk)
        if team.department_id == user_department:
            return True
        return False


