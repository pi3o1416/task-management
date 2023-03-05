
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from department.models import Department
from department.permissions import IsBelongToDepartment
from task.permissions import IsTaskOwner, CanViewAllTasks
from task.models import Task
from services.views import TemplateAPIView, TemplateViewSet
from services.pagination import CustomPageNumberPagination
from .permissions import CanCreateDepartmentTask, CanManageDepartmentTask, IsDepartmentTaskOwner
from .permissions import IsBelongToDepartmentTaskDepartment
from .serializers import DepartmentTaskSerializer, DepartmentTaskCreateAssignSerializer
from .serializers import DepartmentTaskDetailSerializer, DepartmentTaskUpdateSerializer
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
            response_serializer = self.serializer_class(instance=department_task)
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
            response_serializer = self.serializer_class(instance=department_task)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignedOnDepartmentTaskList(TemplateAPIView, CustomPageNumberPagination):
    """
    Assigned on department task list
    """
    model = Department
    serializer_class = DepartmentTaskDetailSerializer
    permission_classes = [CanViewAllTasks|(IsBelongToDepartment&CanManageDepartmentTask)]

    def get(self, request, department_pk):
        department = self.get_object(pk=department_pk)
        department_tasks = department.department_tasks.select_related('task').\
            filter_from_query_params(request=request)
        page = self.paginate_queryset(queryset=department_tasks, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)


class AssignedToDepartmentTaskList(TemplateAPIView, CustomPageNumberPagination):
    """
    User assigned to department task list
    """
    model = User
    serializer_class = DepartmentTaskDetailSerializer
    permission_classes = [CanViewAllTasks|IsAuthenticated]

    def get(self, request, user_pk):
        user = self.get_object(pk=user_pk)
        department_tasks = DepartmentTask.objects.user_department_tasks(
            user=user
        ).filter_from_query_params(request=request)
        page = self.paginate_queryset(queryset=department_tasks, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)


class AuthUserAssignedToDepartmentTasks(TemplateAPIView, CustomPageNumberPagination):
    """
    Authenticated user assigned to department task list
    """
    serializer_class = DepartmentTaskDetailSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        department_tasks = DepartmentTask.objects.user_department_tasks(
            user=request.user
        ).filter_from_query_params()
        page = self.paginate_queryset(queryset=department_tasks, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)


class DepartmentTaskOperationsViewSet(TemplateViewSet):
    model = DepartmentTask

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
        return DepartmentTaskUpdateSerializer

    def get_permissions(self):
        permissions = []
        if self.action in ['submit_task', 'start_task']:
            permissions += [IsBelongToDepartmentTaskDepartment, CanManageDepartmentTask]
        elif self.action in ['accept_submission', 'reject_submission', 'update']:
            permissions += [IsDepartmentTaskOwner]
        return [permission() for permission in permissions]







