
from rest_framework import serializers

from ..models import ProjectMember


class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = ['pk', 'project', 'member', 'member_username', 'member_fullname']
        read_only_fields = ['pk', 'member', 'member_username', 'member_fullname']












