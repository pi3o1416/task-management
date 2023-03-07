
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TeamViewSet, TeamTaskCreateAndAssign, TeamTasksDetail, TeamTasksList, TasksOfTeamList
from .views import DepartmentTeams


team_router = DefaultRouter()
team_router.register('', TeamViewSet, 'team')


app_name='team'
urlpatterns = [
    path('tasks/', TeamTasksList.as_view(), name='task-list'),
    path('tasks/<int:team_task_pk>/', TeamTasksDetail.as_view(), name='team-task-detail'),
    path('<int:team_pk>/create-and-assign-task/', TeamTaskCreateAndAssign.as_view(), name='team-task-create-assign'),
    path('<int:team_pk>/tasks/', TasksOfTeamList.as_view(), name='tasks-of-team'),
    path('department-teams/<int:department_pk>/', DepartmentTeams.as_view(), name='department_teams'),
    path('', include(team_router.urls)),
]




