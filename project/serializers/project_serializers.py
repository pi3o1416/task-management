
from rest_framework import serializers

from ..models import Project, ProjectSchemaLessData


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['pk', 'title', 'description', 'deadline', 'budget', 'project_manager',
                  'project_owner', 'department', 'status']
        read_only_fields = ['pk', 'status']

    def update(self):
        assert self.instance != None, "Initialize serializer with a project instance before update"
        assert self.validated_data != None, "Validate serializer data before update"
        self.instance = Project.update(instance_pk=self.instance.pk, **self.validated_data)
        return self.instance


class ProjectSchemaLessDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSchemaLessData
        fields = ['department_title', 'project_owner_username', 'project_owner_fullname',
                  'project_manager_username', 'project_manager_fullname']
        read_only_fields = ['department_title', 'project_owner_username', 'project_owner_fullname',
                  'project_manager_username', 'project_manager_fullname']


class ProjectDetailSerializer(serializers.ModelSerializer):
    schemaless_data = ProjectSchemaLessDataSerializer()

    class Meta:
        model = Project
        fields = ['pk', 'title', 'description', 'deadline', 'budget', 'project_manager',
                  'project_owner', 'department', 'status', 'schemaless_data']
        read_only_fields = ['pk', 'title', 'description', 'deadline', 'budget', 'project_manager',
                  'project_owner', 'department', 'status', 'schemaless_data']











