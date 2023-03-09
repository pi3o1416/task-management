
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Team
from ..exceptions import MemberBulkAddFailed, MemberBulkRemoveFailed


User = get_user_model()


class MemberSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    photo = serializers.URLField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()


class TeamMemberAddSerializer(serializers.Serializer):
    team_members = serializers.ListField(
        child = serializers.IntegerField()
    )
    member_instances = None

    def validate_team_members(self, team_members):
        users = User.objects.filter(pk__in=team_members)
        if len(users) != len(team_members):
            raise MemberBulkAddFailed(
                detail=_("Invalid member primary key provided")
            )
        self.member_instances = users
        return team_members

    def add_members(self, team:Team):
        assert self.validated_data != None, "Validate serializer before add members"
        assert self.member_instances != None, "Validate serializer before add members"
        assert team.pk != None, "Save team object before adding members"
        team.members.add(*self.member_instances)
        return self.member_instances


class TeamMemberRemoveSerilaizer(serializers.Serializer):
    team_members = serializers.ListField(
        child = serializers.IntegerField()
    )
    member_instances = None

    def validate_team_members(self, team_members):
        users = User.objects.filter(pk__in=team_members)
        if len(users) != len(team_members):
            raise MemberBulkRemoveFailed(
                detail=_("Invalid member primary key provided")
            )
        self.member_instances = users
        return team_members

    def remove_members(self, team:Team):
        assert self.validated_data != None, "Validate serializer before remove member"
        assert self.member_instances != None, "Validate serializer before remove member"
        assert team.pk != None, "Save team object before adding members"
        team.members.remove(*self.member_instances)
        return True



