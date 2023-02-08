
from rest_framework import serializers

from ..models import Project, ProjectSchemaLessData


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['pk', 'title', 'description', 'deadline', 'budget', 'project_manager',
                  'project_owner', 'department', 'status']
        read_only_fields = ['pk', 'status']


class ProjectSchemaLessDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSchemaLessData
        fields = ['department_title', 'project_owner_username', 'project_owner_fullname',
                  'project_manager_username', 'project_manager_fullname']
        read_only_fields = ['department_title', 'project_owner_username', 'project_owner_fullname',
                  'project_manager_username', 'project_manager_fullname']

class ProjectDetailSerializer(serializers.ModelSerializer):
    extended_data = ProjectSchemaLessDataSerializer()

    class Meta:
        model = Project
        fields = ['pk', 'title', 'description', 'deadline', 'budget', 'project_manager',
                  'project_owner', 'department', 'status', 'extended_data']
        read_only_fields = ['pk', 'title', 'description', 'deadline', 'budget', 'project_manager',
                  'project_owner', 'department', 'status', 'extended_data']











