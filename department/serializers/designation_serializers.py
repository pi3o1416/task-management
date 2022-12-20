
from rest_framework import serializers
from ..models import Designations

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designations
        fields = ['pk', 'department', 'title']
        read_only_fields = ['pk']

    def update(self):
        assert self.validated_data, "Call is_valid method before update"
        assert self.instance, "Initialize seirlaizer with department instance"
        self.instance.update(**self.validated_data)


class DesignationPaginatedSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.URLField()
    previous = serializers.URLField()
    results = DesignationSerializer(many=True)






