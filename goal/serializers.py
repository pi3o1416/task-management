
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Goal, Review


User = get_user_model()


class EmptySerializer(serializers.Serializer):
    pass


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ['pk', 'created_by', 'status', 'completion']

    def create(self, created_by, commit=True):
        assert self.validated_data != None, "Validate serializer before create goal instance"
        goal = Goal.create_factory(created_by=created_by, commit=commit, **self.validated_data)
        return goal


class GoalReviewSerializer(serializers.ModelSerializer):
    review = serializers.CharField(required=True)

    class Meta:
        model=Goal
        fields = '__all__'
        read_only_fields = ['pk', 'created_by', 'department', 'title', 'description', 'year',
                            'quarter', 'completion']

    def add_review(self, instance, validated_data):
        review = self.validated_data.get('review')
        instance.add_review(review)
        return True


class GoalPercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Goal
        fields = '__all__'
        read_only_fields = ['pk', 'created_by', 'department', 'title', 'description', 'year',
                            'quarter', 'status']

    def update_percentage(self, instance):
        completion = self.validated_data.get('completion')
        instance.update_completion_percentage(completion)
        return True


class GoalUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Goal
        fields = '__all__'
        read_only_fields = ['pk', 'created_by', 'department', 'status', 'completion']

    def update(self):
        assert self.instance != None, "Initialize serializer with an instance before update"
        assert self.validated_data != None, "Validate serializer before update"
        goal = self.instance.update(**self.validated_data)
        return goal


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['pk', 'goal', 'review', 'reviewed_by', 'reviewed_at']
        read_only_fields = ['pk', 'reviewed_at', 'reviewed_by', 'goal']

    def create(self, reviewed_by:User, goal:Goal, commit=True):
        assert self.validated_data != None, "Validate serializer before add review"
        review = Review.create_factory(
            commit=commit,
            reviewed_by=reviewed_by,
            goal=goal, **self.validated_data
        )
        return review




class GoalDetailSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    class Meta:
        model = Goal
        fields = ['pk', 'created_by', 'department', 'title', 'description', 'year', 'quarter',
                  'status', 'completion', 'reviews']
        read_only_fields = ['pk', 'created_by', 'department', 'title', 'description', 'year',
                            'quarter', 'status', 'completion', 'reviews']

    def get_reviews(self, goal):
        goal_reviews = goal.reviews.all()
        review_serializer = ReviewSerializer(instance=goal_reviews, many=True)
        return review_serializer.data









