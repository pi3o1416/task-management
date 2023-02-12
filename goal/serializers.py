
from rest_framework import serializers

from .models import Goal


class EmptySerializer(serializers.Serializer):
    pass

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['pk', 'department', 'title', 'description', 'year', 'quarter', 'review_status', 'review', 'completion']
        read_only_fields = ['pk', 'review_status', 'review', 'completion', 'department']

    def create(self, commit=True):
        assert self.validated_data != None, "Validate serializer before create goal instance"
        goal = Goal.create_factory(commit=commit, **self.validated_data)
        return goal


class GoalReviewSerializer(serializers.ModelSerializer):
    review = serializers.CharField(required=True)
    class Meta:
        model=Goal
        fields = ['pk', 'department', 'title', 'description', 'year', 'quarter', 'review_status', 'review', 'completion']
        read_only_fields = ['pk', 'department', 'title', 'description', 'year', 'quarter', 'review_status', 'completion']

    def add_review(self, instance, validated_data):
        review = self.validated_data.get('review')
        instance.add_review(review)
        return True


class GoalPercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Goal
        fields = ['pk', 'department', 'title', 'description', 'year', 'quarter', 'review_status', 'review', 'completion']
        read_only_fields = ['pk', 'department', 'title', 'description', 'year', 'quarter', 'review_status', 'review']

    def update_percentage(self, instance):
        completion = self.validated_data.get('completion')
        instance.update_completion_percentage(completion)
        return True


class GoalUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Goal
        fields = ['pk', 'department', 'title', 'description', 'year', 'quarter', 'review_status', 'review', 'completion']
        read_only_fields = ['pk', 'department', 'review_status', 'review']


