
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from services.views import TemplateViewSet, TemplateAPIView
from services.pagination import CustomPageNumberPagination
from department.models import Department
from department.permissions import IsBelongToDepartment
from .models import Goal
from .serializers import GoalDetailSerializer, GoalSerializer, EmptySerializer, GoalReviewSerializer
from .serializers import GoalUpdateSerializer, GoalPercentageSerializer, ReviewSerializer
from .permissions import CanCreateGoal, CanViewGoal, CanViewAllGoals, IsGoalAndUserDepartmentSame
from .permissions import CanChangeGoal, CanDeleteGoal, CanChangeGoalStatus, CanAddReview

class GoalViewSet(TemplateViewSet, CustomPageNumberPagination):
    model = Goal

    def create(self, request):
        user = request.user
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.create(created_by=user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        goals = Goal.objects.filter_from_query_params(request)
        page = self.paginate_queryset(queryset=goals, request=request)
        serializer = self.get_serializer_class()(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)

    def retrieve(self, request, pk):
        goal = self.get_object(pk=pk)
        serializer = self.get_serializer_class()(instance=goal)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        goal = self.get_object(pk=pk)
        serializer = self.get_serializer_class()(instance=goal, data=request.data)
        if serializer.is_valid():
            serializer.update()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response({"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        goal = self.get_object(pk=pk)
        goal.delete()
        return Response(data={"detail": [_("Goal Delete Successful")]}, status=status.HTTP_202_ACCEPTED)

    @action(methods=["patch"], detail=True, url_path='accept-goal')
    def accept_goal(self, request, pk):
        goal = self.get_object(pk=pk)
        goal.accept_goal()
        return Response(data={"detail": [_("Goal accepted")]}, status=status.HTTP_200_OK)

    @action(methods=["patch"], detail=True, url_path='reject-goal')
    def reject_goal(self, request, pk):
        goal = self.get_object(pk=pk)
        goal.reject_goal()
        return Response(data={"detail": [_("Goal pending status set")]}, status=status.HTTP_200_OK)

    @action(methods=["patch"], detail=True, url_path='update-achivement-percentage')
    def update_achivement_percentage(self, request, pk):
        goal = self.get_object(pk=pk)
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.update_percentage(instance=goal)
            return Response(data={"detail": [_("Goal completion percentage update successful")]}, status=status.HTTP_202_ACCEPTED)
        return Response(data={"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        permissions = []
        if self.action == 'create':
            permissions += [CanCreateGoal]
        elif self.action == 'list':
            permissions += [CanViewAllGoals]
        elif self.action == 'retrieve':
            permissions += [CanViewAllGoals|(IsGoalAndUserDepartmentSame&CanViewGoal)]
        elif self.action == 'destroy':
            permissions += [CanDeleteGoal, IsGoalAndUserDepartmentSame]
        elif self.action in ['accept_goal', 'reject_goal']:
            permissions += [CanChangeGoalStatus, CanViewAllGoals]
        elif self.action in ['update_achivement_percentage', 'update']:
            permissions += [CanChangeGoal, IsGoalAndUserDepartmentSame]
        return [permission() for permission in permissions]

    def get_serializer_class(self):
        if self.action in ['reject_goal', 'accept_goal']:
            return EmptySerializer
        elif self.action == 'update_achivement_percentage':
            return GoalPercentageSerializer
        elif self.action == 'update':
            return GoalUpdateSerializer
        elif self.action == 'add_review_on_goal':
            return GoalReviewSerializer
        elif self.action == 'retrieve':
            return GoalDetailSerializer
        return GoalSerializer


class DepartmentGoals(TemplateAPIView, CustomPageNumberPagination):
    model = Department
    serializer_class = GoalSerializer
    permission_classes = [CanViewAllGoals|(IsBelongToDepartment&CanViewGoal)]

    def get(self, request, department_pk):
        department = self.get_object(pk=department_pk)
        department_goals = Goal.objects.get_departmnet_goals(department=department)
        filtered_department_goals = department_goals.filter_from_query_params(request)
        page = self.paginate_queryset(queryset=filtered_department_goals, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)


class AddReviewView(TemplateAPIView):
    model = Goal
    serializer_class = ReviewSerializer
    permission_classes = [CanAddReview|(IsGoalAndUserDepartmentSame&CanViewGoal)]

    def post(self, request, goal_pk):
        goal = self.get_object(pk=goal_pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            review = serializer.create(reviewed_by=request.user, goal=goal)
            response_serializer = self.serializer_class(instance=review)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


