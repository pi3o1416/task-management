
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action

from ..models import TeamMember, Team
from ..serializers import TeamMemberSerializer, TeamMemberBulkAddDeleteSerializer


class TeamMemberViewSet(ViewSet, PageNumberPagination):
    def create(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            team_member = serializer.create(validated_data=serializer.validated_data)
            updated_serializer = self.get_serializer_class()(instance=team_member)
            return Response(data=updated_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        team_members = TeamMember.objects.filter_from_query_params(request)
        page = self.paginate_queryset(queryset=team_members, request=request)
        serializer = self.get_serializer_class()(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)

    def retrieve(self, request, pk):
        team_member = self.get_object(pk)
        serializer = self.get_serializer_class()(instance=team_member)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        team_member = self.get_object(pk)
        team_member.delete()
        return Response(data={"detail": _("Team member delete successful")}, status=status.HTTP_202_ACCEPTED)

    def get_object(self, pk):
        team_member = TeamMember.objects.get_object_by_pk(pk)
        return team_member

    def get_serializer_class(self):
        return TeamMemberSerializer


class GetMembersOfTeam(APIView, PageNumberPagination):
    serializer_class = TeamMemberSerializer

    def get(self, request, team_pk):
        team = self.get_object(team_pk)
        team_members = team.team_members.filter_from_query_params(request)
        page = self.paginate_queryset(queryset=team_members, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)

    def get_object(self, team_pk):
        team = Team.objects.get_team_by_pk(team_pk)
        return team


class BulkAddTeamMember(APIView):
    serializer_class = TeamMemberBulkAddDeleteSerializer

    def post(self, request, team_pk):
        team = self.get_object(team_pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            team_members = serializer.create(team=team, commit=True)
            new_serializer = TeamMemberSerializer(instance=team_members, many=True)
            return Response(data=new_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, team_pk):
        team = Team.objects.get_team_by_pk(team_pk)
        return team



