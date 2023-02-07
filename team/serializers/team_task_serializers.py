
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ..models import TeamTasks, Team
from services.exceptions import DBOperationFailed
from task.serializers import TaskSerializer
from task.models import Task


User = get_user_model()

class TeamTasksCreateAssignSerializer(TaskSerializer):

    def create(self, team:Team, user):
        assert self.validated_data != None, "Validate serializer before create instance"
        task = super().create(commit=False)
        task.created_by = user
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


