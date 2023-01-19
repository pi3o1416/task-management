
from rest_framework import serializers
from .task_serializers import TaskSerializer
from ..models import UsersTasks


class UsersTasksSerializers(serializers.ModelSerializer):
    task = TaskSerializer()
    class Meta:
        model = UsersTasks
        fields = '__all__'


