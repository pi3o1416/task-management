
from rest_framework import serializers

from ..models import Task, TaskTree


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'created_by_user_username',
                            'created_by_user_fullname', 'approved_by_dept_head', 'status']




