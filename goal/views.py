
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from .models import Goal
from .serializers import GoalSerializer, EmptySerializer, GoalReviewSerializer


class GoalViewSet(ViewSet, PageNumberPagination):
    def create(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        goals = Goal.objects.filter_from_query_params(request)
        page = self.paginate_queryset(queryset=goals, request=request)
        serializer = self.get_serializer_class()(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)

    def retrieve(self, request, pk):
        goal = Goal.objects.get_goal_by_pk(pk)
        serializer = self.get_serializer_class()(instance=goal)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        goal = Goal.objects.get_goal_by_pk(pk)
        serializer = self.get_serializer_class()(instance=goal, data=request.data)
        if serializer.is_valid():
            serializer.update(instance=goal, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response({"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        goal = Goal.objects.get_goal_by_pk(pk)
        goal.safe_delete()
        return Response(data={"detail": [_("Goal Delete Successful")]})

    @action(methods=["patch"], detail=True, url_path='accept-goal')
    def accept_goal(self, request, pk):
        goal = Goal.objects.get_goal_by_pk(pk)
        goal.accept_goal()
        return Response(data={"detail": [_("Goal accepted")]})

    @action(methods=["patch"], detail=True, url_path='reject-goal')
    def reject_goal(self, request, pk):
        goal = Goal.objects.get_goal_by_pk(pk)
        goal.set_status_pending()
        return Response(data={"detail": [_("Goal pending status set")]})

    @action(methods=["patch"], detail=True, url_path='add-review')
    def review_on_goal(self, request, pk):
        goal = Goal.objects.get_goal_by_pk(pk)
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.add_review(instance=goal, validated_data=serializer.validated_data)
            return Response(data={"detail": [_("Rview set successful")]})
        return Response(data={"field_errors": serializer.errors})


    def get_serializer_class(self):
        if self.action == 'accept_goal':
            return EmptySerializer
        elif self.action == 'review_on_goal':
            return GoalReviewSerializer
        return GoalSerializer








