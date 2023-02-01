
from rest_framework import serializers

from ..models import TeamMember


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['pk', 'team', 'member', 'member_full_name', 'member_username']
        read_only_fields = ['member_full_name', 'member_username']










