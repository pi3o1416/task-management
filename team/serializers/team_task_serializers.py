
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import TeamTasks, Team
from services.exceptions import DBOperationFailed
from task.serializers import TaskSerializer
from task.models import Task


User = get_user_model()


class TeamInternalTaskCreateSerializer(serializers.ModelSerializer):
    assigned_to = serializers.IntegerField(required=False)
    task = TaskSerializer()

    class Meta:
        model = TeamTasks
        fields = ['pk', 'task', 'team', 'assigned_to']
        read_only_fields = ['pk', 'team']

    def validate_assigned_to(self, assigned_to):
        try:
            user = User.objects.get(pk=assigned_to)
            return user
        except User.DoesNotExist:
            raise ValidationError(detail="Assigned to user does not exist")


    def create(self, team:Team, created_by):
        assert self.validated_data != None, "Validate serializer before create instance"
        assigned_to = self.validated_data.pop('assigned_to')
        task_data = self.validated_data.pop('task')
        task = Task.create_factory(
            created_by=created_by,
            task_type=Task.TaskType.TEAM_TASK,
            **task_data
        )



        task = Task.create_factory(created_by=created_by)
        task.update(task_type = Task.TaskType.TEAM_TASK, commit=True)
        team_task = TeamTasks.create_factory( commit=True, task=task, team=team)
        return team_task


class TeamTasksCreateAssignSerializer(TaskSerializer):
    def create(self, team:Team, user):
        assert self.validated_data != None, "Validate serializer before create instance"
        task = super(created_by=user).create(commit=False)
        task.task_type=Task.TaskType.TEAM_TASK
        task.save()
        team_task = TeamTasks.create_factory(commit=True, task=task, team=team)
        return team_task

    def _create_task(self, task_data, user):
        try:
            task = Task.create_factory(commit=False, **task_data)
            task.created_by = user
            task.save()
            return task
        except Exception as exception:
            raise DBOperationFailed(detail={"detail": _(exception.__str__())})


class TeamTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamTasks
        fields = ['pk', 'team', 'task']


class TeamTasksDetailSerializer(serializers.ModelSerializer):
    task = TaskSerializer()
    class Meta:
        model = TeamTasks
        fields = ['pk', 'team', 'task']


