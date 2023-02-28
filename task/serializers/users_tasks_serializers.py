
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ..models import UsersTasks, Task
from .task_serializers import TaskSerializer


User = get_user_model()


class UsersTasksSerializers(serializers.ModelSerializer):
    class Meta:
        model = UsersTasks
        fields = ['assigned_to']

    def create(self, task, commit=True):
        assert self.validated_data != None, "Validate serializer before creating instance."
        user_task = UsersTasks.create_factory(commit=False, **self.validated_data)
        user_task.task = task
        if commit == True:
            user_task.save()
        return user_task


class UsersTasksDetailSerializer(serializers.ModelSerializer):
    task = TaskSerializer()
    class Meta:
        model = UsersTasks
        fields = '__all__'
        read_only_fields = ['assigned_to', 'task']


class UsersTasksCreateAndAssignSerializer(serializers.ModelSerializer):
    task = TaskSerializer()
    assigned_to = serializers.IntegerField()
    class Meta:
        model = UsersTasks
        fields = ['task', 'assigned_to']

    def create(self, validated_data, user):
        task_data = validated_data.pop('task')
        assigned_to = validated_data.pop('assigned_to')
        task = self._create_task(task_data=task_data, user=user)
        user_task = self._assign_task(task, assigned_to)
        return user_task

    def _create_task(self, task_data, user):
        task = Task.create_factory(commit=False, **task_data)
        task.update(is_assigned=True, commit=False)
        task.set_task_owner(created_by=user, commit=True)
        return task

    def _assign_task(self, task, assigned_to_pk):
        assigned_to_user = User.objects.get_object_by_pk(assigned_to_pk)
        user_task = UsersTasks.create_factory(task=task, assigned_to=assigned_to_user)
        return user_task













