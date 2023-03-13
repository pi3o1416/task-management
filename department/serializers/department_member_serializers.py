
from django.forms import model_to_dict
from django.contrib.auth import get_user_model
from rest_framework import serializers

from department.serializers.department_serializers import DepartmentMinimalSerializer
from ..models import DepartmentMember, Department


User = get_user_model()


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

    def update(self):
        assert self.validated_data, "Call is_valid method before update"
        assert self.instance, "Initialize seirlaizer with department instance"
        self.instance.update(**self.validated_data)




class UserSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    photo = serializers.URLField()


class DepartmentMemberDetailSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = DepartmentMember
        fields = ['pk', 'member', 'department', 'designation', 'department_name', 'designation_title']
        read_only_fields = ['pk', 'department_name', 'designation_title']

    def get_member(self, department_member):
        member_pk = model_to_dict(department_member, fields=['member']).get('member')
        member = User.objects.get_object_from_cache(pk=member_pk)
        serializer = UserSerializer(instance=member)
        return serializer.data

    def get_department(self, department_member):
        department_pk = model_to_dict(department_member, fields=['department']).get('department')
        department = Department.objects.get_object_from_cache(pk=department_pk)
        serializer = DepartmentMinimalSerializer(instance=department)
        return serializer.data


class DepartmentMemberPaginatedSerializer(serializers.Serializer):
    """
    Only for documentation
    """
    count = serializers.IntegerField()
    next = serializers.URLField()
    previous = serializers.URLField()
    results = DepartmentMemberSerializer(many=True)



