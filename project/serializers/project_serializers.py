
from django.forms import model_to_dict
from django.contrib.auth import get_user_model
from rest_framework import serializers

from department.models import Department
from ..models import Project, ProjectAttachment


User = get_user_model()


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


class DepartmentMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = Department.CACHED_FIELDS


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = User.CACHED_FIELDS



class ProjectDetailSerializer(serializers.ModelSerializer):
    project_manager = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    project_owner = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['pk', 'title', 'description', 'deadline', 'budget', 'project_manager',
                  'project_owner', 'department', 'status']
        read_only_fields = ['pk', 'title', 'description', 'deadline', 'budget', 'project_manager',
                  'project_owner', 'department', 'status']

    def get_project_manager(self, project):
        project_manager_pk = model_to_dict(instance=project, fields=['project_manager']).get('project_manager')
        project_manager = User.objects.get_object_from_cache(pk=project_manager_pk)
        serializer = UserMinimalSerializer(instance=project_manager)
        return serializer.data

    def get_department(self, project):
        department_pk = model_to_dict(instance=project, fields=['department']).get('department')
        department = Department.objects.get_object_from_cache(pk=department_pk)
        serializer = DepartmentMinimalSerializer(instance=department)
        return serializer.data

    def get_project_owner(self, project):
        project_owner_pk = model_to_dict(instance=project, fields=['project_manager']).get('project_manager')
        project_owner = User.objects.get_object_from_cache(pk=project_owner_pk)
        serializer = UserMinimalSerializer(instance=project_owner)
        return serializer.data


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












