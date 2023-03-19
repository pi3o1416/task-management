
from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from task.serializers import TaskSerializer, TaskDetailSerializer
from task.models import Task, UsersTasks
from task.exceptions import TaskCreateFailed, UserTasksCreateFailed
from team.querysets import TeamTasksQuerySet
from ..models import TeamTasks, Team
from ..exceptions import TeamTaskCreateFailed, TeamInternalTaskCreateFailed
from .team_serializers import TeamDetailSerializer


User = get_user_model()


class TeamTasksCreateAssignSerializer(serializers.ModelSerializer):
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
            user_task = TeamTasks.create_and_assign_root_task(
                assigned_to=assigned_to,
                commit=True,
                team=team,
                task=task
            )
            return user_task
        except (TaskCreateFailed, UserTasksCreateFailed, TeamTaskCreateFailed) as exception:
            raise TeamInternalTaskCreateFailed(detail=exception.__str__())


class TeamInternalTaskCreateSerializer(TaskSerializer):
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
            team_task = TeamTasks.create_root_task(commit=True, task=task, team=team)
            return team_task
        except (TaskCreateFailed, TeamTaskCreateFailed) as exception:
            raise TeamTaskCreateFailed(detail=exception.__str__())


class AssignTaskToTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamTasks
        fields = ['team']

    def create(self, task, commit=True):
        assert self.validated_data != None, "Validate serializer before create team task"
        team = self.validated_data.get('team')
        team_task = TeamTasks.assign_task_on_team(team=team, task=task, commit=True)
        return team_task


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


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = User.CACHED_FIELDS


class TeamTasksDetailWithAssignedToUserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        user_tasks = UsersTasks.objects.filter(task__pk__in=instance.values('pk')).values('task', 'assigned_to')
        self.user_tasks = {user_task['task']: user_task['assigned_to'] for user_task in user_tasks}
        super().__init__(*args, **kwargs)

    task = TaskDetailSerializer()
    team = serializers.SerializerMethodField()
    assigned_to = serializers.SerializerMethodField()

    class Meta:
        model = TeamTasks
        fields = ['pk', 'team', 'task', 'assigned_to']

    def get_team(self, value):
        team_pk = value.team_id
        team = Team.objects.get_object_from_cache(pk=team_pk)
        serializer = TeamDetailSerializer(instance=team)
        return serializer.data

    def get_assigned_to(self, value):
        task = value.task_id
        if task in self.user_tasks:
            assigned_to_user_pk = self.user_tasks[task]
            user = User.objects.get_object_from_cache(pk=assigned_to_user_pk)
            serializer = UserMinimalSerializer(instance=user)
            return serializer.data
        return None








