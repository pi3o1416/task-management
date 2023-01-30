
from rest_framework import serializers

from ..models import Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['pk', 'title', 'description', 'department', 'team_lead', 'team_lead_full_name']
        read_only_fields = ['pk', 'department', 'team_lead_full_name']

    def create(self, commit=True):
        assert self.validated_data != None, "Validate serializer before create team instance"
        team_instance = Team.create_factory(**self.validated_data, commit=commit)
        return team_instance


class TeamUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['pk', 'title', 'description', 'department', 'team_lead', 'team_lead_full_name']
        read_only_fields = ['pk', 'department', 'team_lead_full_name']

    def update(self):
        assert self.validated_data != None, "Validate serializer before update"
        assert self.instance != None, "Initialize serilaizer with team instance"
        assert type(self.instance) is Team, "Instance should be an instance of team"
        self.instance.update(**self.validated_data)



