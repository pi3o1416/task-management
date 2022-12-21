
from rest_framework import serializers
from ..models import DepartmentMember


class DepartmentMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentMember
        fields = ['pk', 'member', 'department', 'designation', 'department_name', 'designation_title', 'member_full_name']
        read_only_fields = ['pk', 'department_name', 'designation_title', 'member_full_name']


class DepartmentMemberUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentMember
        fields = ['pk', 'member', 'department', 'designation', 'department_name', 'designation_title', 'member_full_name']
        read_only_fields = ['pk', 'member', 'department_name', 'designation_title', 'member_full_name']


class DepartmentMemberPaginatedSerializer(serializers.Serializer):
    """
    Only for documentation
    """
    count = serializers.IntegerField()
    next = serializers.URLField()
    previous = serializers.URLField()
    results = DepartmentMemberSerializer(many=True)


