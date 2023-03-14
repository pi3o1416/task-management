
from django.db import transaction
from django.forms import model_to_dict
from rest_framework import serializers

from task.serializers import TaskSerializer, TaskDetailSerializer
from department.models import Department
from .models import DepartmentTask, Task


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

