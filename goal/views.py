
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from department.models import Department
from .models import Goal
from .serializers import GoalSerializer, EmptySerializer, GoalReviewSerializer, GoalUpdateSerializer, GoalPercentageSerializer


class GoalViewSet(ViewSet, PageNumberPagination):
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
        return Response(data={"detail": [_("Goal Delete Successful")]}, status=status.HTTP_202_ACCEPTED)

    @action(methods=["patch"], detail=True, url_path='accept-goal')
    def accept_goal(self, request, pk):
        goal = Goal.objects.get_goal_by_pk(pk)
        goal.accept_goal()
        return Response(data={"detail": [_("Goal accepted")]}, status=status.HTTP_200_OK)

    @action(methods=["patch"], detail=True, url_path='reject-goal')
    def reject_goal(self, request, pk):
        goal = Goal.objects.get_goal_by_pk(pk)
        goal.set_status_pending()
        return Response(data={"detail": [_("Goal pending status set")]}, status=status.HTTP_200_OK)

    @action(methods=["patch"], detail=True, url_path='add-review')
    def add_review_on_goal(self, request, pk):
        goal = Goal.objects.get_goal_by_pk(pk)
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.add_review(instance=goal, validated_data=serializer.validated_data)
            return Response(data={"detail": [_("Rview set successful")]}, status=status.HTTP_200_OK)
        return Response(data={"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["patch"], detail=True, url_path='update-achivement-percentage')
    def update_achivement_percentage(self, request, pk):
        goal = Goal.objects.get_goal_by_pk(pk)
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.update_percentage(instance=goal)
            return Response(data={"detail": [_("Goal completion percentage update successful")]}, status=status.HTTP_202_ACCEPTED)
        return Response(data={"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action in ['reject_goal', 'accept_goal']:
            return EmptySerializer
        elif self.action == 'update_achivement_percentage':
            return GoalPercentageSerializer
        elif self.action == 'update':
            return GoalUpdateSerializer
        elif self.action == 'add_review_on_goal':
            return GoalReviewSerializer
        return GoalSerializer


class DepartmentGoals(APIView):
    serializer_class = GoalSerializer
    def get(self, request, department_pk):
        department = Department.objects.get_department(department_pk)
        department_goals = Goal.objects.get_departmnet_goals(department=department)
        filtered_department_goals = department_goals.filter_from_query_params(request)
        serializer = self.serializer_class(instance=filtered_department_goals, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class GoalCreateView(APIView):
    serializer_class = GoalSerializer
    def post(self, request, department_pk):
        department = Department.objects.get_department(department_pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            goal = serializer.create(commit=False)
            goal.department = department
            goal.save()
            response_serializer = GoalSerializer(instance=goal)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response({"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)














