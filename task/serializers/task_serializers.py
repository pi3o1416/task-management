
from rest_framework import serializers

from ..models import Task, TaskTree


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'created_by_user_username',
                            'created_by_user_fullname', 'approved_by_dept_head', 'status']

    def create(self, commit=True):
        assert self.validated_data != None, "Validated serialzier before create object"
        task = Task(**self.validated_data)
        if commit == True:
            task.save()
        return task




