
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .task_serializers import TaskSerializer
from ..models import TaskTree, Task
from ..exceptions import DBOperationFailed


class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['pk', 'created_by', 'title', 'description', 'created_at', 'last_date',
                  'approval_status', 'status', 'priority', 'created_by_user_username',
                  'created_by_user_fullname']
        read_only_fields = ['pk', 'created_by', 'created_at', 'created_by_user_username',
                            'created_by_user_fullname', 'approval_status', 'status']

    def create(self, user, commit=True):
        assert self.validated_data != None, "Validate serializer before create instance"
        task = self.create_subtask(self.validated_data, user, commit=commit)
        return task

    def create_subtask(self, task_data, user, commit=True):
        task = Task.create_factory(commit=False, **task_data)
        task.update_task_owner(user=user, commit=commit)
        return task

    def create_task_tree(self, child, parent, commit=True):
        task_tree = TaskTree.create_factory(commit=commit, parent=parent, child=child)
        return task_tree



class TaskTreeDetailSerializer(serializers.Serializer):
    parent = TaskSerializer()
    child = TaskSerializer()


