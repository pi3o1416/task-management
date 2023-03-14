
from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from rest_framework import serializers

from ..models import Task, TaskAttachments

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['pk', 'created_by', 'title', 'description', 'created_at', 'last_date',
                  'approval_status', 'status', 'priority']
        read_only_fields = ['pk', 'created_by', 'created_at', 'approval_status', 'status']

    def create(self, created_by, commit=True):
        assert self.validated_data != None, "Validated serialzier before create object"
        task = Task.create_factory(created_by=created_by, commit=commit, **self.validated_data)
        return task

    def update(self, instance, commit = True):
        assert self.validated_data != None, "Validate serializer before update"
        assert type(instance) is Task, "Should be an instance of Task model"
        instance.update(commit=commit, **self.validated_data)
        return instance


class TaskStatusStatisticsSerializer(serializers.Serializer):
    status = serializers.CharField()
    count = serializers.IntegerField()

    @property
    def final_data(self):
        final_data = self.data
        breakpoint()
        return final_data


class TaskAttachmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAttachments
        fields = ['pk', 'task', 'attached_by', 'attachment', 'attached_at']
        read_only_fields = ['pk', 'attached_by', 'attached_at', 'task']


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = User.CACHED_FIELDS

class TaskDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = ['pk', 'created_by', 'title', 'description', 'created_at', 'last_date',
                  'approval_status', 'status', 'priority']

    def get_created_by(self, task):
        created_by_pk = model_to_dict(task, fields=['created_by']).get('created_by')
        created_by = User.objects.get_object_from_cache(pk=created_by_pk)
        serializer = UserMinimalSerializer(instance=created_by)
        return serializer.data

