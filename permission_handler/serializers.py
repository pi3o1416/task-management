
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ['pk', 'app_label', 'model']
        read_only_fields = ['pk', 'app_label', 'model']


class PermissionSerializer(serializers.ModelSerializer):
    content_type = ContentTypeSerializer()
    class Meta:
        model = Permission
        fields = ['pk', 'name', 'content_type', 'codename']
        read_only_fields = ['pk', 'name', 'content_type', 'codename']


class PermissionMinimalSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    name = serializers.CharField()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class GroupDetailSerializer(serializers.ModelSerializer):
    permissions = PermissionMinimalSerializer(many=True)
    class Meta:
        model = Group
        fields = '__all__'





