
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from services.views import TemplateAPIView
from task.models import Task
from task.serializers import SubTaskCreateSerializer
from ..serializers import TeamTasksCreateAssignSerializer, TeamTasksSerializer, TeamTasksDetailSerializer
from ..serializers import TeamInternalTaskCreateSerializer
from ..models import Team, TeamTasks


class TeamInternalTaskCreate(TemplateAPIView):
    model = Team
    serializer_class = TeamInternalTaskCreateSerializer

    def post(self, request, team_pk):
        team = self.get_object(pk=team_pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            team_task = serializer.create(team=team, created_by=request.user)
            response_serializer = TeamTasksSerializer(instance=team_task)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)


class TeamTaskCreateAndAssign(TemplateAPIView):
    model = Team
    serializer_class = TeamTasksCreateAssignSerializer

    def post(self, request, team_pk):
        team = self.get_object(pk=team_pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            team_member = serializer.create(team=team, user=request.user)
            new_serializer = TeamTasksSerializer(instance=team_member)
            return Response(data=new_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class TeamTasksDetail(APIView):
    serializer_class = TeamTasksDetailSerializer

    def get(self, request, team_task_pk):
        team_task = self.get_object(team_task_pk)
        serializer = self.serializer_class(instance=team_task)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_object(self, pk):
        return TeamTasks.objects.get_object_by_pk(pk)


class TeamTasksList(APIView, PageNumberPagination):
    """
    List of all teams tasks
    """
    serializer_class = TeamTasksDetailSerializer

    def get(self, request):
        teams_tasks = TeamTasks.objects.filter_with_related_fields(request)
        page = self.paginate_queryset(queryset=teams_tasks, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)


class TasksOfTeamList(APIView, PageNumberPagination):
    """
    List of all tasks of a team
    """
    serializer_class = TeamTasksDetailSerializer

    def get(self, request, team_pk):
        team = self.get_object(pk=team_pk)
        team_tasks = team.team_tasks.all().filter_with_related_fields(request=request)
        page = self.paginate_queryset(queryset=team_tasks, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)

    def get_object(self, pk):
        return Team.objects.get_object_by_pk(pk)


class AssignTeamTasksToMembers(APIView):
    """
    Assign tasks assigned to a team to a perticular team member
    """
    serializer_class = SubTaskCreateSerializer

    def post(self, request, team_pk, task_pk):
        team = self.get_object(team_pk)
        task = Task.objects.get_task_by_pk(task_pk)
        serializer = self.serializer_class(data=request.data)


    def get_object(self, pk):
        return Team.objects.get_object_by_pk(pk)




