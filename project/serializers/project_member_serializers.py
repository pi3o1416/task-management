
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from services.exceptions import InvalidRequest
from ..models import Project

User = get_user_model()


class ProjectMemberSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()


class ProjectMemberBulkCreateSerializer(serializers.Serializer):
    project_members = serializers.ListSerializer(
        child=serializers.IntegerField()
    )
    member_instances = None

    error_messages = {
        "BULK_CREATE": "Project bulk create failed."
    }

    def validate_project_members(self, project_members):
        users = User.objects.filter(pk__in=project_members)
        if len(users) != len(project_members):
            raise ValidationError(_("Invalid member primary key"))
        self.member_instances = users
        return project_members

    def create(self, project:Project, commit=True):
        assert self.validated_data != None, "Validate serializer before create model instance"
        assert self.member_instances != None, "Validate serializer before create model instance"
        assert project.pk != None, "Save the project object before adding project member"
        project.members.add(*self.member_instances.values_list('pk', flat=True))
        return self.member_instances






