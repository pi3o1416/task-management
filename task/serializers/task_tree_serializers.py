
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .task_serializers import TaskSerializer
from ..models import TaskTree, Task
from ..exceptions import DBOperationFailed


class TaskTreeCreateSerializer(serializers.ModelSerializer):
    child = TaskSerializer()
    class Meta:
        model = TaskTree
        fields = ['parent', 'child']

    def create(self, user, commit=True):
        assert self.validated_data != None, "Validate serializer before create instance"
        child = self.validated_data.get("child")
        parent = self.validated_data.get("parent")
        sub_task = self.create_subtask(child, user)
        task_tree = TaskTree.create_factory(commit=commit, parent=parent, child=sub_task)
        return task_tree

    def create_subtask(self, task_data, user):
        try:
            task = Task.create_factory(commit=False, **task_data)
            task.created_by = user
            task.save()
            return task
        except Exception as exception:
            raise DBOperationFailed(detail={"detail": _(exception.__str__())})


class TaskTreeDetailSerializer(serializers.Serializer):
    parent = TaskSerializer()
    child = TaskSerializer()


