
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .task_serializers import TaskSerializer
from ..models import TaskTree, Task


class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['pk', 'created_by', 'title', 'description', 'created_at', 'last_date',
                  'approval_status', 'status', 'priority']
        read_only_fields = ['pk', 'created_by', 'created_at', 'approval_status', 'status']

    def create(self, created_by, parent_task, commit=True):
        assert self.validated_data != None, "Validate serializer before create instance"
        task = self.create_subtask(self.validated_data, created_by, commit=commit)
        tree_edge = self.create_task_tree_edge(parent=parent_task, child=task)
        return tree_edge

    def create_subtask(self, task_data, user, commit=True):
        task = Task.create_factory(commit=False, **task_data)
        task.set_task_owner(created_by=user, commit=commit)
        return task

    def create_task_tree_edge(self, child, parent, commit=True):
        task_tree = TaskTree.create_factory(commit=commit, parent=parent, child=child)
        return task_tree



class TaskTreeDetailSerializer(serializers.Serializer):
    parent = TaskSerializer()
    child = TaskSerializer()


