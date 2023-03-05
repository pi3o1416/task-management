
from rest_framework import serializers

from task.serializers import TaskSerializer
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


class DepartmentTaskDetailSerializer(serializers.ModelSerializer):
    task = TaskSerializer()
    class Meta:
        model = DepartmentTask
        fields = ['pk', 'task', 'department']
        read_only_fields = ['pk', 'task', 'department']


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









