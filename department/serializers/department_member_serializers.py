
from rest_framework import serializers
from ..models import DepartmentMember


class DepartmentMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentMember
        fields = ['pk', 'member', 'department', 'designation', 'department_name', 'designation_title']
        read_only_fields = ['pk', 'department_name', 'designation_title']


class DepartmentMemberUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentMember
        fields = ['pk', 'member', 'department', 'designation', 'department_name', 'designation_title']
        read_only_fields = ['pk', 'member', 'department_name', 'designation_title']


class UserSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    photo = serializers.URLField()


class DepartmentMemberDetailSerializer(serializers.ModelSerializer):
    member = UserSerializer()
    class Meta:
        model = DepartmentMember
        fields = '__all__'


class DepartmentMemberPaginatedSerializer(serializers.Serializer):
    """
    Only for documentation
    """
    count = serializers.IntegerField()
    next = serializers.URLField()
    previous = serializers.URLField()
    results = DepartmentMemberSerializer(many=True)



