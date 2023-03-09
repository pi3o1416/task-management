
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response

from services.pagination import CustomPageNumberPagination
from services.views import TemplateViewSet, TemplateAPIView
from department.models import Department
from department.permissions import IsBelongToDepartment
from ..serializers import TeamSerializer, TeamUpdateSerializer
from ..permissions import CanViewAllTeams, CanCreateTeam
from ..permissions import CanDeleteTeam, CanChangeTeam
from ..models import Team


class TeamViewSet(TemplateViewSet, CustomPageNumberPagination):
    model = Team

    def create(self, request):
        user = request.user
        user_department = user.user_department.department
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            team = serializer.create(department=user_department)
            response_serializer = self.get_serializer_class()(instance=team)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        teams = Team.objects.filter_from_query_params(request=request)
        page = self.paginate_queryset(queryset=teams, request=request)
        serializer = self.get_serializer_class()(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)

    def retrieve(self, request, pk):
        team = self.get_object(pk=pk)
        serializer = self.get_serializer_class()(instance=team)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        team = self.get_object(pk)
        team.delete()
        return Response(data={"detail": _("Team delete successful")}, status=status.HTTP_202_ACCEPTED)

    def update(self, request, pk):
        team = self.get_object(pk)
        serializer = self.get_serializer_class()(instance=team, data=request.data)
        if serializer.is_valid():
            serializer.update()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        permissions = []
        if self.action == 'create':
            permissions += [CanCreateTeam]
        elif self.action == 'list':
            permissions += [CanViewAllTeams]
        elif self.action == 'retrieve':
            permissions += [CanViewAllTeams]
        elif self.action == 'destroy':
            permissions += [CanDeleteTeam]
        elif self.action == 'update':
            permissions += [CanChangeTeam]
        return [permission() for permission in permissions]

    def get_serializer_class(self):
        if self.action == 'update':
            return TeamUpdateSerializer
        return TeamSerializer


class DepartmentTeams(TemplateAPIView, CustomPageNumberPagination):
    model = Department
    serializer_class = TeamSerializer
    permission_classes = [IsBelongToDepartment, CanCreateTeam]

    def get(self, request, department_pk):
        department = self.get_object(pk=department_pk)
        dept_teams = department.departmetn_teams.all().filter_from_query_params(request=request)
        page = self.paginate_queryset(queryset=dept_teams, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)




