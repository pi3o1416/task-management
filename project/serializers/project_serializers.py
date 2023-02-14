
from rest_framework import serializers

from ..models import Project, ProjectSchemaLessData, ProjectAttachment


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['pk', 'title', 'description', 'deadline', 'budget', 'project_manager',
                  'project_owner', 'department', 'status']
        read_only_fields = ['pk', 'status']

    def update(self):
        assert self.instance != None, "Initialize serializer with a project instance before update"
        assert self.validated_data != None, "Validate serializer data before update"
        self.instance.update(commit=True, **self.validated_data)
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


class ProjectAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAttachment
        fields = ['pk', 'project', 'attached_by', 'attachment', 'attached_at',
                  'attached_by_user_username', 'attached_by_user_fullname']
        read_only_fields = ['pk', 'project', 'attached_by', 'attached_at',
                            'attached_by_user_username', 'attached_by_user_fullname']

    def create(self, commit=True):
        assert self.validated_data != None, "Validate serializer before create instance"
        project_attachment = ProjectAttachment.create_factory(
            commit=commit,
            **self.validated_data
        )
        return project_attachment












