
from rest_framework import serializers
from ..models import UsersTasks


class UsersTasksSerializers(serializers.ModelSerializer):
    class Meta:
        model = UsersTasks
        fields = '__all__'
        read_only_fields = ['assigned_to', 'user_username', 'user_full_name']




