
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from services.pagination import CustomPageNumberPagination
from services.views import TemplateViewSet, TemplateAPIView
from department.permissions import IsSameDepartment
from ..serializers import UsersTasksSerializers, UsersTasksDetailSerializer, UsersTasksCreateAssignSerializer
from ..models import UsersTasks, Task
from ..permissions import IsTaskOwner, CanViewInterDepartmentTask, CanCreateTask, CanViewAllTasks
from ..permissions import CanCreateUsersTasks, IsUserTaskOwner


User = get_user_model()


class UsersTasksViewSet(TemplateViewSet, CustomPageNumberPagination):
    model = UsersTasks

    def list(self, request):
        """
        List of all tasks
        """
        tasks = UsersTasks.objects.select_related('task').filter_from_query_params(request)
        page = self.paginate_queryset(queryset=tasks, request=request)
        serializer = self.get_serializer_class()(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)

    def destroy(self, request, pk):
        """
        Destroy specific task assignment
        """
        user_task = self.get_object(pk)
        user_task.delete()
        return Response(data={"detail": _("User Task destroy successful")})

    def get_permissions(self):
        permission_classes = []
        if self.action == 'list':
            permission_classes += [CanViewAllTasks]
        elif self.action == 'destroy':
            permission_classes += [IsUserTaskOwner]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'assign':
            return UsersTasksSerializers
        if self.action in ['list', 'retrieve']:
            return UsersTasksDetailSerializer
        return UsersTasksSerializers


class UserTaskAssign(TemplateAPIView):
    """
    Assign a user previously created task.
    """
    model = Task
    serializer_class = UsersTasksSerializers
    permission_classes = [IsTaskOwner, CanCreateUsersTasks]

    def post(self, request, task_pk):
        task = self.get_object(pk=task_pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_task = serializer.create(task=task)
            response_serializer = self.serializer_class(instance=user_task)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersTasksCreateAndAssign(TemplateAPIView):
    """
    Create a new task and assign it to a user.
    """
    serializer_class = UsersTasksCreateAssignSerializer
    permission_classes = [CanCreateTask]

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_task = serializer.create(created_by=user)
            response_serializer = UsersTasksDetailSerializer(instance=user_task)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={"field_errors": serializer.errors})


class UserTasksList(TemplateAPIView, CustomPageNumberPagination):
    """
    API view to get user specific task list
    """
    model = User
    permission_classes = [IsSameDepartment, CanViewInterDepartmentTask]
    serializer_class = UsersTasksDetailSerializer

    def get(self, request, user_pk):
        user = self.get_object(pk=user_pk)
        user_tasks = user.user_tasks.select_related('task').all()
        filtered_user_tasks = user_tasks.filter_with_task(request)
        page = self.paginate_queryset(queryset=filtered_user_tasks, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)


class AuthUserAssignedUserTasks(TemplateAPIView, CustomPageNumberPagination):
    """
    API View to get user created user tasks.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UsersTasksDetailSerializer

    def get(self, request):
        user = request.user
        user_tasks = UsersTasks.objects.select_related('task').filter(task__created_by=user)\
            .filter_from_query_params(request=request)
        page = self.paginate_queryset(queryset=user_tasks, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)


class AuthUserAssignedUponUserTasks(TemplateAPIView, CustomPageNumberPagination):
    """
    API View to get list of all user assigned upon user tasks
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UsersTasksDetailSerializer

    def get(self, request):
        user = request.user
        assigned_upon_user_tasks = user.user_tasks.all().filter_from_query_params(request=request)
        page = self.paginate_queryset(queryset=assigned_upon_user_tasks, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)


class DepartmentUserTasks(TemplateAPIView, CustomPageNumberPagination):
    serializer_class = UsersTasksDetailSerializer
    permission_classes = [CanViewAllTasks|(IsSameDepartment, CanViewInterDepartmentTask)]

    def get(self, request, department_pk):
        department_members_task = UsersTasks.objects.department_based_tasks(department_pk)
        filtered_tasks = department_members_task.filter_from_query_params(request=request)
        page = self.paginate_queryset(queryset=filtered_tasks, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)




