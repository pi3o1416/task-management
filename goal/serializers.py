
from rest_framework import serializers

from .models import Goal


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['pk', 'department', 'title', 'description', 'year', 'quarter', 'review_status', 'review', 'completion']
        read_only_fields = ['pk', 'review_status', 'review', 'completion']







