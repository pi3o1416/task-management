
from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from task.serializers import TaskSerializer, TaskDetailSerializer
from task.models import Task, UsersTasks
from task.exceptions import TaskCreateFailed, UserTasksCreateFailed
from ..models import TeamTasks, Team
from ..exceptions import TeamTaskCreateFailed, TeamInternalTaskCreateFailed
from .team_serializers import TeamDetailSerializer


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

    @transaction.atomic
    def create(self, team:Team, created_by):
        try:
            assert self.validated_data != None, "Validate serializer before create instance"
            assigned_to = self.validated_data.pop('assigned_to')
            task_data = self.validated_data.pop('task')
            task = Task.create_factory(
                created_by=created_by,
                task_type=Task.TaskType.TEAM_TASK,
                is_assigned=True,
                **task_data
            )
            TeamTasks.create_factory(
                commit=True,
                task=task,
                team=team,
                internal_task=True
            )
            user_task = UsersTasks.create_factory(commit=True, assigned_to=assigned_to, task=task)
            return user_task
        except (TaskCreateFailed, UserTasksCreateFailed, TeamTaskCreateFailed) as exception:
            raise TeamInternalTaskCreateFailed(detail=exception.__str__())


class TeamTasksCreateAssignSerializer(TaskSerializer):
    @transaction.atomic
    def create(self, team:Team, created_by):
        try:
            assert self.validated_data != None, "Validate serializer before create instance"
            task = Task.create_factory(
                commit=True,
                created_by=created_by,
                is_assigned=True,
                task_type=Task.TaskType.TEAM_TASK,
                **self.validated_data
            )
            team_task = TeamTasks.create_factory(
                commit=True,
                task=task,
                team=team,
                internal_task=False
            )
            return team_task
        except (TaskCreateFailed, TeamTaskCreateFailed) as exception:
            raise TeamTaskCreateFailed(detail=exception.__str__())


class TeamTaskAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamTasks
        fields = ['team']

    def create(self, task):
        assert self.validated_data != None, "Validate serializer before create team task"
        if task.task_type == Task.TaskType.TEAM_TASK:
            team_task = TeamTasks.objects.filter(task=task).update(
                team=self.validated_data.get('team')
            )
        #TODO:


class TeamTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamTasks
        fields = ['pk', 'team', 'task']


class TeamTasksDetailSerializer(serializers.ModelSerializer):
    task = TaskDetailSerializer()
    team = serializers.SerializerMethodField()

    class Meta:
        model = TeamTasks
        fields = ['pk', 'team', 'task']

    def get_team(self, value):
        team_pk = value.team_id
        team = Team.objects.get_object_from_cache(pk=team_pk)
        serializer = TeamDetailSerializer(instance=team)
        return serializer.data







