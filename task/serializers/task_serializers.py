
from rest_framework import serializers

from ..models import Task, TaskTree


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'




