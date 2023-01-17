
from django.contrib.auth.models import Permission
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



