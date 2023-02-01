
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from rest_framework import serializers

from services.exceptions import DBOperationFailed, InvalidRequest
from ..models import TeamMember

User = get_user_model()


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['pk', 'team', 'member', 'member_full_name', 'member_username']
        read_only_fields = ['member_full_name', 'member_username']

class TeamMemberBulkAddDeleteSerializer(serializers.Serializer):
    member = serializers.ListField(
        child=serializers.IntegerField()
    )

    def create(self, team, commit=True):
        try:
            assert self.validated_data != None, "Validate serializer before create model instance."
            members = self.validated_data.get('member')
            team_members = self.generate_team_members(members=members, team=team)
            if commit == True:
                team_members = TeamMember.objects.bulk_create_team_member(team_members)
            return team_members
        except IntegrityError as exception:
            raise InvalidRequest(detail={"detail": _(exception.__str__())})

    def generate_team_members(self, members, team):
        user_instances = User.objects.filter(pk__in=members)
        if len(user_instances) != len(members):
            raise InvalidRequest(detail="All members primary keys are not valid")
        return [TeamMember.create_factory(commit=False, member=user, team=team) for user in user_instances]






