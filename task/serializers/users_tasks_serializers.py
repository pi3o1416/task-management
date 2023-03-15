
from django.db import transaction
from django.forms import model_to_dict
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ..models import UsersTasks, Task
from .task_serializers import TaskSerializer, TaskDetailSerializer, UserMinimalSerializer


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
    task = TaskDetailSerializer()
    assigned_to = serializers.SerializerMethodField()
    class Meta:
        model = UsersTasks
        fields = '__all__'
        read_only_fields = ['assigned_to', 'task']

    def get_assigned_to(self, user_task):
        assigned_to_user_pk = model_to_dict(user_task, fields=['assigned_to']).get('assigned_to')
        assigned_to = User.objects.get_object_from_cache(pk=assigned_to_user_pk)
        serializer = UserMinimalSerializer(instance=assigned_to)
        return serializer.data


class UsersTasksCreateAssignSerializer(serializers.ModelSerializer):
    task = TaskSerializer()
    assigned_to = serializers.IntegerField()
    class Meta:
        model = UsersTasks
        fields = ['task', 'assigned_to']

    @transaction.atomic
    def create(self, created_by):
        assert self.validated_data != None, "Validate serializer before create"
        task_data = validated_data.pop('task')
        assigned_to = validated_data.pop('assigned_to')
        task = Task.create_factory(
            commit=True,
            created_by=created_by,
            **task_data
        )
        user_task = self._assign_task(task, assigned_to)
        return user_task

    def _assign_task(self, task, assigned_to_pk):
        assigned_to_user = User.objects.get_object_by_pk(assigned_to_pk)
        user_task = UsersTasks.create_factory(task=task, assigned_to=assigned_to_user)
        return user_task













