
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from services.pagination import CustomPageNumberPagination
from services.views import TemplateAPIView
from ..models import Team
from ..serializers import MemberSerializer, TeamSerializer, TeamMemberAddSerializer
from ..serializers import TeamMemberRemoveSerilaizer
from ..permissions import IsTeamLeadOfTeam, CanViewAllTeams, IsTeamAndUserDepartmentSame
from ..permissions import CanCreateTeam, CanChangeTeam


class TeamMembersList(TemplateAPIView, CustomPageNumberPagination):
    model = Team
    serializer_class = MemberSerializer
    permission_classes = [IsTeamLeadOfTeam|(IsTeamAndUserDepartmentSame|CanCreateTeam)|CanViewAllTeams]

    def get(self, request, team_pk):
        team = self.get_object(pk=team_pk)
        members = team.members.all().filter_from_query_params(request=request)
        page = self.paginate_queryset(queryset=members, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)


class AuthUserTeamList(TemplateAPIView, CustomPageNumberPagination):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_teams = Team.objects.member_teams(member=user).filter_from_query_params()
        page = self.paginate_queryset(queryset=user_teams, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)


class AuthUserLeadTeams(TemplateAPIView, CustomPageNumberPagination):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        team_lead = request.user
        leading_teams = team_lead.leading_teams.select_realted('department').all()
        page = self.paginate_queryset(queryset=leading_teams, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)

class AddTeamMembers(TemplateAPIView):
    model = Team
    serializer_class = TeamMemberAddSerializer
    permission_classes = [IsTeamAndUserDepartmentSame, (CanCreateTeam|CanChangeTeam)]

    def get(self, request, team_pk):
        team = self.get_object(pk=team_pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            members = serializer.add_members(team=team)
            response_serializer = MemberSerializer(instance=members, many=True)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteTeamMembers(TemplateAPIView):
    model = Team
    serializer_class = TeamMemberRemoveSerilaizer
    permission_classes = [IsTeamAndUserDepartmentSame, (CanCreateTeam|CanChangeTeam)]

    def delete(self, request, team_pk):
        team = self.get_object(pk=team_pk)
        serializer = self.serializer_class(team=team, action='remove', data=request.data)
        if serializer.is_valid():
            serializer.remove_members(team=team)
            return Response(data=_("Members delete successful"), status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

