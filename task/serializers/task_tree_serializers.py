
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .task_serializers import TaskSerializer
from ..models import TaskTree, Task
from ..exceptions import TaskCreateFailed, TaskTreeCreateFailed


class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['pk', 'created_by', 'title', 'description', 'created_at', 'last_date',
                  'approval_status', 'status', 'priority']
        read_only_fields = ['pk', 'created_by', 'created_at', 'approval_status', 'status']

    @transaction.atomic
    def create(self, created_by, parent_task:Task, commit=True):
        try:
            assert self.validated_data != None, "Validate serializer before create instance"
            assert parent_task.pk != None, "Save parent task before creating child task"
            child_task = Task.create_factory(
                created_by=created_by,
                commit=True,
                task_type=parent_task.task_type,
                **self.validated_data
            )
            tree_edge = TaskTree.create_factory(commit=commit, parent=parent_task, child=child_task)
            return tree_edge
        except (TaskCreateFailed, TaskTreeCreateFailed) as exception:
            raise TaskTreeCreateFailed(exception.__str__())


class TaskTreeDetailSerializer(serializers.Serializer):
    parent = TaskSerializer()
    child = TaskSerializer()


