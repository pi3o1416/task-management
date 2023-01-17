
from authentication.models import CustomUser
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ['pk', 'app_label', 'model']
        read_only_fields = ['pk', 'app_label', 'model']


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['pk', 'name', 'codename']
        read_only_fields = ['pk', 'name', 'codename']


class PermissionDetailSerializer(serializers.ModelSerializer):
    content_type = ContentTypeSerializer()
    class Meta:
        model = Permission
        fields = ['pk', 'name', 'codename', 'content_type']
        read_only_fields = ['pk', 'name', 'codename', 'content_type']



class PermissionMinimalSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    name = serializers.CharField()
    codename = serializers.CharField()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class GroupDetailSerializer(serializers.ModelSerializer):
    permissions = PermissionMinimalSerializer(many=True)
    class Meta:
        model = Group
        fields = '__all__'


class GroupAssignSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    group = serializers.IntegerField()

    def validate_user(self, value):
        user = CustomUser.objects.filter(pk=value).first()
        if user != None:
            return user
        raise ValidationError(_("User with pk={} does not exist".format(value)))

    def validate_group(self, value):
        group = Group.objects.filter(pk=value).first()
        if group != None:
            return group
        raise ValidationError(_("Group with pk={} does not exist".format(value)))

    def save(self):
        assert self.validated_data != None, "Validate serializer assign group"
        breakpoint()
        group = self.validated_data.get('group')
        user = self.validated_data.get('user')
        group.user_set.add(user.pk)
        return True








