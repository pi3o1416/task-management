
from rest_framework import serializers

from ..models import Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['pk', 'title', 'description', 'team_lead', 'team_lead_username', 'team_lead_first_name', 'team_lead_last_name']
        read_only_fields = ['pk', 'team_lead_username', 'team_lead_first_name', 'team_lead_last_name']
