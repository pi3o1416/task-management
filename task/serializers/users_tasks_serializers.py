
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from task.exceptions import DBOperationFailed
from ..models import UsersTasks, Task
from ..exceptions import DBOperationFailed
from .task_serializers import TaskSerializer


User = get_user_model()


class UsersTasksSerializers(serializers.ModelSerializer):
    class Meta:
        model = UsersTasks
        fields = '__all__'
        read_only_fields = ['user_username', 'user_full_name']


class UsersTasksDetailSerializer(serializers.ModelSerializer):
    task = TaskSerializer()
    class Meta:
        model = UsersTasks
        fields = '__all__'
        read_only_fields = ['assigned_to', 'task', 'user_username', 'user_full_name']


class UsersTasksCreateAndAssignSerializer(serializers.ModelSerializer):
    task = TaskSerializer()
    assigned_to = serializers.IntegerField()
    class Meta:
        model = UsersTasks
        fields = ['task', 'assigned_to']

    def create(self, validated_data, user):
        try:
            task_data = validated_data.pop('task')
            assigned_to = validated_data.pop('assigned_to')
            task = self._create_task(task_data=task_data, user=user)
            user_task = self._assign_task(task, assigned_to)
            return user_task
        except Exception as exception:
            raise DBOperationFailed(detail={"detail": _(exception.__str__())})

    def _create_task(self, task_data, user):
        try:
            task = Task.create_factory(commit=False, **task_data)
            task.created_by = user
            task.save()
            return task
        except Exception as exception:
            raise DBOperationFailed(detail={"detail": _(exception.__str__())})

    def _assign_task(self, task, assigned_to_pk):
        try:
            assigned_to_user = User.objects.get_user_by_pk(assigned_to_pk)
            user_task = UsersTasks.create_factory(commit=False, task=task, assigned_to=assigned_to_user)
            user_task.save()
            return user_task
        except Exception as exception:
            raise DBOperationFailed(detail={"detail": _(exception.__str__())})













