
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TeamViewSet, TeamMemberViewSet, GetMembersOfTeam, BulkAddTeamMember, TeamTaskCreateAndAssign, TeamTasksDetail, TeamTasksList, TasksOfTeamList


team_router = DefaultRouter()
team_router.register('', TeamViewSet, 'team')

team_member_router = DefaultRouter()
team_member_router.register('', TeamMemberViewSet, 'team-member')


app_name='team'
urlpatterns = [
    path('members/', include(team_member_router.urls)),
    path('<int:team_pk>/members/', GetMembersOfTeam.as_view(), name='members-of-team'),
    path('<int:team_pk>/bulk-add-members/', BulkAddTeamMember.as_view(), name='bulk-add-member'),
    path('tasks/', TeamTasksList.as_view(), name='task-list'),
    path('tasks/<int:team_task_pk>/', TeamTasksDetail.as_view(), name='team-task-detail'),
    path('<int:team_pk>/create-and-assign-task/', TeamTaskCreateAndAssign.as_view(), name='team-task-create-assign'),
    path('<int:team_pk>/tasks/', TasksOfTeamList.as_view(), name='tasks-of-team'),
    path('', include(team_router.urls)),
]




