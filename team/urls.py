
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TeamViewSet, TeamTaskCreateAndAssign, TeamTasksList, TeamInternalTaskCreate
from .views import TeamMembersList, AuthUserTeamList, AuthUserLeadTeams, DeleteTeamMembers
from .views import DepartmentTeams, AddTeamMembers


team_router = DefaultRouter()
team_router.register('', TeamViewSet, 'team')


app_name='team'
urlpatterns = [
    path('tasks/', TeamTasksList.as_view(), name='task-list'),
    path('<int:team_pk>/create-and-assign-task/', TeamTaskCreateAndAssign.as_view(), name='team-task-create-assign'),
    path('<int:team_pk>/team-members/', TeamMembersList.as_view(), name='team-members'),
    path('<int:team_pk>/add-members/', AddTeamMembers.as_view(), name='add-members'),
    path('<int:team_pk>/remove-members/', DeleteTeamMembers.as_view(), name='remove-members'),
    path('<int:team_pk>/create-internal-task/', TeamInternalTaskCreate.as_view(), name='team-internal-task-create'),
    path('auth-user-teams/', AuthUserTeamList.as_view(), name='auth-user-team-list'),
    path('auth-user-lead-teams/', AuthUserLeadTeams.as_view(), name='auth-user-lead-teams'),
    path('department-teams/<int:department_pk>/', DepartmentTeams.as_view(), name='department_teams'),
    path('', include(team_router.urls)),
]




