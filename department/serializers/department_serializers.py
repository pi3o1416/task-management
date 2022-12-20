
from django.template.defaultfilters import slugify
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from ..models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['pk', 'name', 'slug', 'description']
        read_only_fields = ['pk', 'slug']

    def validate_name(self, name):
        slug = slugify(name)
        slug_exist = Department.objects.filter(slug=slug).exists()
        if slug_exist:
            raise ValidationError("Slug value generated form this name already exist", code="already-exist")
        return name

    def update(self):
        assert self.validated_data, "Call is_valid method before update"
        assert self.instance, "Initialize seirlaizer with department instance"
        self.instance.update(**self.validated_data)


class DepartmentPaginatedSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.URLField()
    previous = serializers.URLField()
    results = DepartmentSerializer(many=True)







