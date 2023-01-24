
from django.utils.translation import gettext_lazy as _
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action

from ..permissions import CanViewAllTasks, IsOwner, HasPermissionToApproveTask, IsAssignedUponUser
from ..serializers import TaskSerializer
from ..models import Task


class TaskViewSet(ViewSet, PageNumberPagination):
    #TODO: need reapproval from department head on task update
    def create(self, request):
        user = request.user
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            task = serializer.create(commit=False)
            task.update_task_owner(user, commit=False)
            task.save()
            #Update serializer with populate fields.
            serializer = self.get_serializer_class()(instance=task)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        tasks = Task.objects.filter_from_query_params(request)
        page = self.paginate_queryset(queryset=tasks, request=request)
        serializer = self.get_serializer_class()(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)

    def destroy(self, request, pk):
        task = self.get_object(pk)
        self.check_object_permissions(request, task)
        task.delete()
        return Response(data={"detail": [_("Task delete successful")]}, status=status.HTTP_202_ACCEPTED)

    def retrieve(self, request, pk):
        task = self.get_object(pk)
        self.check_object_permissions(request, task)
        serializer = self.get_serializer_class()(instance=task)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        task = self.get_object(pk)
        self.check_object_permissions(request, task)
        serializer = self.get_serializer_class()(instance=task, data=request.data)
        if serializer.is_valid():
            serializer.update(instance=task, validated_data=serializer.validated_data)
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data={"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['patch'], detail=True, url_path='approve-task')
    def approve_task(self, request, pk):
        task = self.get_object(pk)
        task.approve_task()
        return Response(data={"detail": [_("Task with pk={} approved".format(pk))]}, status=status.HTTP_202_ACCEPTED)

    @action(methods=['patch'], detail=True, url_path='disapprove-task')
    def disapprove_task(self, request, pk):
        task = self.get_object(pk)
        task.reject_approval_request()
        return Response(data={"detail": [_("Task with pk={} has been denied")]})

    @action(methods=['patch'], detail=True, url_path='start-task')
    def start_task(self, request, pk):
        task = self.get_object(pk)
        self.check_object_permissions(request, task)
        task.start_task()
        return Response(data={"detail": [_("Task start successful")]})

    @action(methods=['patch'], detail=True, url_path='submit-task')
    def submit_task(self, request, pk):
        task = self.get_object(pk)
        self.check_object_permissions(request, task)
        task.submit_task()
        return Response(data={"detail": [_("Task submission successful")]})

    @action(methods=['patch'], detail=True, url_path='accept-submission')
    def accept_task_submission(self, request, pk):
        task = self.get_object(pk)
        self.check_object_permissions(request, task)
        task.accept_task_submission()
        return Response(data={"detail": [_("Task submission accepted")]})

    @action(methods=['patch'], detail=True, url_path='reject-submission')
    def reject_task_submission(self, request, pk):
        task = self.get_object(pk)
        self.check_object_permissions(request, task)
        task.reject_task_submission()
        return Response(data={"detail": [_("Task submission rejected")]})

    def get_object(self, pk):
        task = Task.objects.get_task_by_pk(pk)
        return task

    def get_serializer_class(self):
        return TaskSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action == 'create':
            permission_classes += []
        elif self.action == 'list':
            permission_classes += [CanViewAllTasks]
        elif self.action == 'retrieve':
            permission_classes += [IsOwner|CanViewAllTasks|IsAssignedUponUser]
        elif self.action in ['destroy', 'update']:
            permission_classes += [IsOwner]
        elif self.action in ['approve_task', 'disapprove_task']:
            permission_classes += [HasPermissionToApproveTask]
        elif self.action in ['start_task', 'submit_task']:
            permission_classes += [IsAssignedUponUser]
        elif self.action in ['accept_task_submission', 'reject_task_submission']:
            permission_classes += [IsOwner]
        return [permission() for permission in permission_classes]






