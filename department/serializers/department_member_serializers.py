
from rest_framework import serializers
from ..models import DepartmentMember


class DepartmentMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentMember
        fields = ['pk', 'member', 'department', 'designation']
        read_only_fields = ['pk']


class DepartmentMemberUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentMember
        fields = ['pk', 'member', 'department', 'designation']
        read_only_fields = ['pk', 'member']


class DepartmentMemberPaginatedSerializer(serializers.Serializer):
    """
    Only for documentation
    """
    count = serializers.IntegerField()
    next = serializers.URLField()
    previous = serializers.URLField()
    results = DepartmentMemberSerializer(many=True)


