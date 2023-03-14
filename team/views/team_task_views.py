
from rest_framework import status
from rest_framework.response import Response

from services.pagination import CustomPageNumberPagination
from services.views import TemplateAPIView
from ..serializers import TeamTasksCreateAssignSerializer, TeamTasksSerializer, TeamTasksDetailSerializer
from ..serializers import TeamInternalTaskCreateSerializer
from ..models import Team, TeamTasks


class TeamInternalTaskCreate(TemplateAPIView):
    """
    Team internal task create and assign
    """
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
    """
    Create a task and assign to a team
    """
    model = Team
    serializer_class = TeamTasksCreateAssignSerializer

    def post(self, request, team_pk):
        team = self.get_object(pk=team_pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            team_member = serializer.create(team=team, created_by=request.user)
            new_serializer = TeamTasksSerializer(instance=team_member)
            return Response(data=new_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class TeamTasksList(TemplateAPIView, CustomPageNumberPagination):
    """
    List of all tasks of a team
    """
    model = Team
    serializer_class = TeamTasksDetailSerializer

    def get(self, request, team_pk):
        team = self.get_object(pk=team_pk)
        team_tasks = TeamTasks.objects.select_related('team').filter(team=team)
        filtered_team_tasks = team_tasks.filter_from_query_params(request=request)
        page = self.paginate_queryset(queryset=filtered_team_tasks, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)


