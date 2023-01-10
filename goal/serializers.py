
from rest_framework import serializers

from .models import Goal


class EmptySerializer(serializers.Serializer):
    pass

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['pk', 'department', 'title', 'description', 'year', 'quarter', 'review_status', 'review', 'completion']
        read_only_fields = ['pk', 'review_status', 'review', 'completion']


class GoalReviewSerializer(serializers.Serializer):
    class Meta:
        model=Goal
        fields = ['pk', 'department', 'title', 'description', 'year', 'quarter', 'review_status', 'review', 'completion']
        read_only_fields = ['pk', 'department', 'title', 'description', 'year', 'quarter', 'review_status', 'completion']

    
    def add_review(self, instance, validated_data):
        review = self.validated_data.get('review')
        instance.add_reivew(review)
        return True









