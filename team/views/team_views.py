
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from ..serializers import TeamSerializer, TeamUpdateSerializer
from ..models import Team


class TeamViewSet(ViewSet, PageNumberPagination):
    def create(self, request):
        breakpoint()
        user = request.user
        user_department = user.user_department.department
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            team = serializer.create(commit=False)
            team.department = user_department
            team.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
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
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


    def get_object(self, pk):
        team = Team.objects.get_object_by_pk(pk)
        return team

    def get_serializer_class(self):
        if self.action == 'update':
            return TeamUpdateSerializer
        return TeamSerializer




