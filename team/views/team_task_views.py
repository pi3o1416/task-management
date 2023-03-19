
from rest_framework import status
from rest_framework.response import Response

from services.pagination import CustomPageNumberPagination
from services.views import TemplateAPIView, TemplateViewSet
from task.serializers import UsersTasksDetailSerializer
from task.permissions import CanViewAllTasks, CanManageExistingTask
from task.models import Task
from ..serializers import TeamTasksCreateAssignSerializer, TeamTasksDetailSerializer
from ..serializers import TeamInternalTaskCreateSerializer, AssignTaskToTeamSerializer
from ..serializers import TeamTasksDetailWithAssignedToUserSerializer
from ..models import Team, TeamTasks
from ..permissions import CanCreateTeamTasks, IsMemberOfTeam, IsTeamAndUserDepartmentSame
from ..permissions import CanManageTeamTasks


class TeamInternalTaskCreate(TemplateAPIView):
    """
    Team internal task create and assign
    """
    model = Team
    serializer_class = TeamInternalTaskCreateSerializer
    permission_classes = [IsMemberOfTeam, CanCreateTeamTasks]

    def post(self, request, team_pk):
        team = self.get_object(pk=team_pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            team_task = serializer.create(team=team, created_by=request.user)
            response_serializer = UsersTasksDetailSerializer(instance=team_task)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)


class TeamTaskCreateAndAssign(TemplateAPIView):
    """
    Create a task and assign to a team
    """
    model = Team
    serializer_class = TeamTasksCreateAssignSerializer
    permission_classes = [CanCreateTeamTasks, IsTeamAndUserDepartmentSame]

    def post(self, request, team_pk):
        team = self.get_object(pk=team_pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            team_member = serializer.create(team=team, created_by=request.user)
            resposne_serializer = TeamTasksDetailSerializer(instance=team_member)
            return Response(data=resposne_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AssignExistingTaskToTeam(TemplateAPIView):
    """
    Assign an already existing task to team
    """
    model = Task
    permission_classes = [CanManageExistingTask]
    serializer_class = AssignTaskToTeamSerializer

    def post(self, request, task_pk):
        task = self.get_object(pk=task_pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            team_task = serializer.create(task=task)
            response_serializer = TeamTasksDetailSerializer(instance=team_task)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamTasksList(TemplateAPIView, CustomPageNumberPagination):
    """
    List of all tasks of a team
    """
    model = Team
    serializer_class = TeamTasksDetailSerializer
    permission_classes = [CanViewAllTasks]

    def get(self, request):
        team_tasks = TeamTasks.objects.select_related('task')
        filtered_team_tasks = team_tasks.filter_from_query_params(request=request)
        page = self.paginate_queryset(queryset=filtered_team_tasks, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)


class TasksOfATeam(TemplateAPIView, CustomPageNumberPagination):
    """
    List of all tasks for a team
    """
    model = Team
    serializer_class = TeamTasksDetailSerializer
    permission_classes = [IsMemberOfTeam, CanManageTeamTasks]

    def get(self, request, team_pk):
        team = self.get_object(pk=team_pk)
        team_tasks = team.team_tasks.select_related('task').all()
        filtered_team_tasks = team_tasks.filter_from_query_params(request=request)
        page = self.paginate_queryset(queryset=filtered_team_tasks, request=request)
        serializer = TeamTasksDetailWithAssignedToUserSerializer(instance=page, many=True)
        self.get_paginated_response(data=serializer.data)








