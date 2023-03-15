
from django.db import transaction
from django.forms import model_to_dict
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from services.exceptions import ObjectNotFound
from team.models import TeamTasks, Team
from task.serializers import TaskSerializer, TaskDetailSerializer
from task.serializers import TaskSerializer
from task.models import UsersTasks, TaskTree
from department.models import Department
from .models import DepartmentTask, Task


User = get_user_model()


class DepartmentTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentTask
        fields = ['pk', 'task', 'department']
        read_only_fields = ['pk', 'task']

    def create(self, task, commit=True):
        assert self.validated_data != None, "Validate serializer before call create method."
        department = self.validated_data.get('department')
        department_task = DepartmentTask.create_factory(
            task=task,
            department=department,
            commit=commit
        )
        return department_task


class DepartmentTaskCreateAssignSerializer(serializers.ModelSerializer):
    task = TaskSerializer()
    class Meta:
        model = DepartmentTask
        fields = ['pk', 'task', 'department']
        read_only_fields = ['pk']

    @transaction.atomic
    def create(self, created_by, commit=True):
        assert self.validated_data != None, "Validate serializer before call create method."
        department = self.validated_data.pop("department")
        task_data = self.validated_data.pop("task")
        task = Task.create_factory(created_by=created_by, commit=True, **task_data)
        department_task = DepartmentTask.create_factory(
            task=task,
            department=department
        )
        return department_task


class DepartmentMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = Department.CACHED_FIELDS


class DepartmentTaskDetailSerializer(serializers.ModelSerializer):
    task = TaskDetailSerializer()
    department = serializers.SerializerMethodField()

    class Meta:
        model = DepartmentTask
        fields = ['pk', 'task', 'department']
        read_only_fields = ['pk', 'task', 'department']

    def get_department(self, department_task):
        department_pk = model_to_dict(department_task, fields=['department']).get('department')
        department = Department.objects.get_object_from_cache(pk=department_pk)
        serializer = DepartmentMinimalSerializer(instance=department)
        return serializer.data


class DepartmentTaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentTask
        fields = ['pk', 'task', 'department']
        read_only_fields = ['pk', 'task']

    def update(self):
        assert self.instance != None, "Initialize serializer with a department task instance"
        assert self.validated_data != None, "Validate serializer before update"
        assert type(self.instance) is DepartmentTask, "Instance should be DepartmentTask type"
        department = self.validated_data.pop('department')
        self.instance.update(department=department)
        return self.instance


class DepartmentSubTaskSerializer(serializers.Serializer):
    task = TaskSerializer()
    assigned_to = serializers.IntegerField()
    team = serializers.IntegerField()

    def __init__(self, action=None, *args, **kwargs):
        self.action = action
        super().__init__(*args, **kwargs)

    def validate_assigned_to(self, value):
        try:
            user = User.objects.get_object_by_pk(pk=value)
            return user
        except ObjectNotFound as exception:
            raise ValidationError(exception.__str__())

    def validate_team(self, value):
        try:
            team = Team.objects.get_object_by_pk(pk=value)
            return team
        except ObjectNotFound as exception:
            raise ValidationError(exception.__str__())

    def get_fields(self):
        assert self.action == None, "Stupid"
        fields = super().get_fields()
        if self.action == 'user_subtask':
            fields.pop('team')
        if self.action == 'team_subtask':
            fields.pop('assigned_to')
        return fields


    @transaction.atomic
    def create(self, created_by, department_task):
        assert self.action in ['user_subtask', 'team_subtask'], "Initialize serializer with action 'user_subtask' or 'team_subtask'"
        assert self.validated_data != None, "Validate serializer before create subtask."
        assert isinstance(created_by, User), "Created by should be an user instance"
        assert isinstance(department_task, DepartmentTask), "Department task should be an DepartmentTask instance"
        task_data = self.validated_data.pop('task')
        #Create child task instance
        child_task = Task.create_factory(commit=True, created_by=created_by, **task_data)
        parent_task = department_task.task
        #Add new task tree instance with parent task and child task
        TaskTree.create_factory(parent=parent_task, child=child_task)
        if self.action == 'user_subtask':
            assigned_to = self.validated_data.pop('assigned_to')
            user_task = UsersTasks.create_factory(assigned_to=assigned_to, task=child_task)
            return user_task
        else:
            team = self.validated_data.pop('team')
            team_task = TeamTasks.create_factory(team=team, task=child_task)
            return team_task


