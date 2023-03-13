
from django.forms import model_to_dict
from django.core.cache import cache
from rest_framework import serializers
from ..models import Designations, Department
from .department_serializers import DepartmentMinimalSerializer

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designations
        fields = ['pk', 'department', 'title']
        read_only_fields = ['pk']

    def update(self):
        assert self.validated_data, "Call is_valid method before update"
        assert self.instance, "Initialize seirlaizer with department instance"
        self.instance.update(**self.validated_data)


class DesignationDetailSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()
    class Meta:
        model = Designations
        fields = ['pk', 'department', 'title']

    def get_department(self, designation):
        department_pk = model_to_dict(designation, fields=['department']).get('department')
        department = Department.objects.get_object_from_cache(pk=department_pk, raise_exception=True)
        serializer = DepartmentMinimalSerializer(instance=department)
        return serializer.data


class DesignationPaginatedSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.URLField()
    previous = serializers.URLField()
    results = DesignationSerializer(many=True)






