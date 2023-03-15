
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from department.models import DepartmentMember
from task.permissions import IsTaskOwner, CanViewAllTasks
from task.models import Task
from team.serializers import TeamTasksDetailSerializer
from services.views import TemplateAPIView, TemplateViewSet
from services.pagination import CustomPageNumberPagination
from task.serializers.users_tasks_serializers import UsersTasksDetailSerializer
from .permissions import CanCreateDepartmentTask, CanManageDepartmentTask, IsDepartmentTaskOwner
from .permissions import IsBelongToDepartmentTaskDepartment
from .serializers import DepartmentTaskSerializer, DepartmentTaskCreateAssignSerializer
from .serializers import DepartmentTaskDetailSerializer, DepartmentTaskUpdateSerializer
from .serializers import DepartmentSubTaskSerializer
from .models import DepartmentTask


User = get_user_model()


class DepartmentTaskAssign(TemplateAPIView):
    """
    Assign a pre created department task
    """
    model = Task
    permission_classes = [IsTaskOwner, CanCreateDepartmentTask]
    serializer_class = DepartmentTaskSerializer

    def post(self, request, task_pk):
        task = self.get_object(pk=task_pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            department_task = serializer.create(task=task, commit=True)
            response_serializer = DepartmentTaskDetailSerializer(instance=department_task)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DepartmentTaskCreateAssign(TemplateAPIView):
    """
    Create and assign department task
    """
    serializer_class = DepartmentTaskCreateAssignSerializer
    permission_classes = [CanCreateDepartmentTask]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            department_task = serializer.create(commit=True, created_by=request.user)
            response_serializer = DepartmentTaskDetailSerializer(instance=department_task)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllDepartmentTaskList(TemplateAPIView, CustomPageNumberPagination):
    """
    List of all department tasks
    """
    serializer_class = DepartmentTaskDetailSerializer
    permission_classes = [CanViewAllTasks]

    def get(self, request):
        department_tasks = DepartmentTask.objects.filter_with_related_fields(
            request=request,
            related_fields = ['task']
        )
        page = self.paginate_queryset(queryset=department_tasks, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)


class AuthUserDepartmentTasksList(TemplateAPIView, CustomPageNumberPagination):
    """
    Authenticated user's department's department task.
    """
    serializer_class = DepartmentTaskDetailSerializer
    permission_classes = [IsAuthenticated, CanManageDepartmentTask]

    def get(self, request):
        user = request.user
        user_department_pk = DepartmentMember.objects.member_department(member_pk=user.pk)
        department_task = DepartmentTask.objects.filter(department=user_department_pk)
        filtered_department_task = department_task.filter_with_related_fields(
            request=request,
            related_fields = ['task']
        )
        page = self.paginate_queryset(queryset=filtered_department_task, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)


class UserAssignedToDepartmentTaskList(TemplateAPIView, CustomPageNumberPagination):
    """
    User assigned to department task list
    """
    model = User
    serializer_class = DepartmentTaskDetailSerializer
    permission_classes = [CanViewAllTasks]

    def get(self, request, user_pk):
        user = self.get_object(pk=user_pk)
        department_tasks = DepartmentTask.objects.user_department_tasks(
            user=user
        ).filter_with_related_fields(request=request, related_fields=['task'])
        page = self.paginate_queryset(queryset=department_tasks, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)


class AuthUserAssignedToDepartmentTasksList(TemplateAPIView, CustomPageNumberPagination):
    """
    Authenticated user assigned to department task list
    """
    serializer_class = DepartmentTaskDetailSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        department_tasks = DepartmentTask.objects.user_department_tasks(
            user=request.user
        ).filter_with_related_fields(request=request, related_fields=['task'])
        page = self.paginate_queryset(queryset=department_tasks, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)


class DepartmentTaskOperationsViewSet(TemplateViewSet):
    model = DepartmentTask

    @action(methods=['post'], detail=True, url_path='create-subtask-and-assign-to-user')
    def create_subtask_assign_to_user(self, request, pk):
        """
        Create subtask from department task and assign to user
        """
        department_task = self.get_object(pk=pk)
        serializer = self.get_serializer_class()(action='user_subtask', data=request.data)
        if serializer.is_valid():
            user_task = serializer.create(created_by=request.user, department_task=department_task)
            response_serializer = UsersTasksDetailSerializer(instance=user_task)
            return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, url_path='create-subtask-and-assign-to-team')
    def create_subtask_assign_to_team(self, request, pk):
        """
        Create subtask from department task and assign to team
        """
        department_task = self.get_object(pk=pk)
        serializer = self.get_serializer_class()(action='team_subtask', data=request.data)
        if serializer.is_valid():
            team_task = serializer.create(created_by=request.user, department_task=department_task)
            response_serializer = TeamTasksDetailSerializer(instance=team_task)
            return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], detail=True, url_path='update')
    def update_task(self, request, pk):
        """
        Update department task
        """
        department_task = self.get_object(pk=pk)
        serializer = self.get_serializer_class()(instance=department_task, data=request.data)
        if serializer.is_valid():
            department_task = serializer.update()
            response_serializer = DepartmentTaskDetailSerializer(instance=department_task)
            return Response(data=response_serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['patch'], detail=True, url_path='submit')
    def submit_task(self, request, pk):
        """
        Submit department task
        """
        department_task = self.get_object(pk=pk)
        task = department_task.task
        task.update(status=Task.StatusChoices.SUBMITTED)
        return Response(data=_("Department task submission successful"))

    @action(methods=['patch'], detail=True, url_path='start-task')
    def start_task(self, request, pk):
        """
        Start department task
        """
        department_task = self.get_object(pk=pk)
        task = department_task.task
        task.update(status=Task.StatusChoices.DUE)
        return Response(data=_("Department task start successful"))

    @action(methods=['patch'], detail=True, url_path='accept-submission')
    def accept_submission(self, request, pk):
        """
        Accept department task submission
        """
        department_task = self.get_object(pk=pk)
        task = department_task.task
        task.update(status=Task.StatusChoices.COMPLETED)
        return Response(data=_("Department task submission accepted"))

    @action(methods=['patch'], detail=True, url_path='reject-submission')
    def reject_submission(self, request, pk):
        """
        Reject department task submission
        """
        department_task = self.get_object(pk=pk)
        task = department_task.task
        task.update(status=Task.StatusChoices.DUE)
        return Response(data=_("Department task submission rejected"))

    def get_serializer_class(self):
        if self.action == 'create_subtask_assign_to_user':
            return DepartmentSubTaskSerializer
        if self.action == 'create_subtask_assign_to_team':
            return DepartmentSubTaskSerializer
        return DepartmentTaskUpdateSerializer

    def get_permissions(self):
        permissions = []
        if self.action in ['submit_task', 'start_task']:
            permissions += [IsBelongToDepartmentTaskDepartment, CanManageDepartmentTask]
        elif self.action in ['accept_submission', 'reject_submission', 'update']:
            permissions += [IsDepartmentTaskOwner]
        return [permission() for permission in permissions]







