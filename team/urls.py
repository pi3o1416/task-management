
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TeamViewSet, TeamTaskCreateAndAssign, TeamTasksDetail, TeamTasksList
from .views import TasksOfTeamList, TeamMembersList, AuthUserTeamList, AuthUserLeadTeams
from .views import DepartmentTeams, AddTeamMembers, DeleteTeamMembers


team_router = DefaultRouter()
team_router.register('', TeamViewSet, 'team')


app_name='team'
urlpatterns = [
    path('tasks/', TeamTasksList.as_view(), name='task-list'),
    path('tasks/<int:team_task_pk>/', TeamTasksDetail.as_view(), name='team-task-detail'),
    path('<int:team_pk>/create-and-assign-task/', TeamTaskCreateAndAssign.as_view(), name='team-task-create-assign'),
    path('<int:team_pk>/tasks/', TasksOfTeamList.as_view(), name='tasks-of-team'),
    path('<int:team_pk>/team-members/', TeamMembersList.as_view(), name='team-members'),
    path('<int:team_pk>/add-members/', AddTeamMembers.as_view(), name='add-members'),
    path('<int:team_pk>/remove-members/', DeleteTeamMembers.as_view(), name='remove-members'),
    path('auth-user-teams/', AuthUserTeamList.as_view(), name='auth-user-team-list'),
    path('auth-user-lead-teams/', AuthUserLeadTeams.as_view(), name='auth-user-lead-teams'),
    path('department-teams/<int:department_pk>/', DepartmentTeams.as_view(), name='department_teams'),
    path('', include(team_router.urls)),
]




