
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import action

from services.pagination import CustomPageNumberPagination
from services.views import TemplateViewSet, TemplateAPIView
from ..permissions import CanViewAllTasks, IsTaskAssignee, IsTaskOwner, IsTaskParents
from ..permissions import HasPermissionToApproveTask, CanCreateTask, CanDeleteTask, CanUpdateTask
from ..permissions import IsAttachmentOwner, CanManageExistingTask
from ..serializers import TaskSerializer, TaskAttachmentsSerializer, TaskStatusStatisticsSerializer
from ..models import Task, TaskAttachments


class TaskViewSet(TemplateViewSet, CustomPageNumberPagination):
    #TODO: need reapproval from department head on task update
    model = Task

    def create(self, request):
        """
        Create new task
        """
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            task = serializer.create(created_by=request.user)
            response_serializer = TaskSerializer(instance=task)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            data={"field_errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def list(self, request):
        """
        List of all tasks
        """
        tasks = Task.objects.filter_from_query_params(request)
        page = self.paginate_queryset(queryset=tasks, request=request)
        serializer = self.get_serializer_class()(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)

    @action(methods=['get'], detail=False, url_path="all-task-statistics")
    def task_list_statistics(self, request):
        """
        Task status statistics
        """
        tasks = Task.objects.filter_from_query_params(request)
        tasks_statistics = tasks.get_task_status_statistics()
        serializer = self.get_serializer_class()(instance=tasks_statistics, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        """
        Delete task with maintaining proper restriction
        """
        task = self.get_object(pk)
        task.delete()
        return Response(
            data={"detail": [_("Task delete successful")]},
            status=status.HTTP_202_ACCEPTED
        )

    @action(methods=['delete'], detail=True, url_path='force-delete')
    def force_destroy(self, request, pk):
        """
        Delete task avoiding any restriction
        """
        task = self.get_object(pk)
        task.delete()
        return Response(
            data={"detail": _("Task delete successful")},
            status=status.HTTP_202_ACCEPTED
        )

    def retrieve(self, request, pk):
        """
        Retrieve Task by primary key
        """
        task = self.get_object(pk)
        serializer = self.get_serializer_class()(instance=task)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        """
        Update a task instance
        """
        task = self.get_object(pk)
        serializer = self.get_serializer_class()(instance=task, data=request.data)
        if serializer.is_valid():
            serializer.update(instance=task)
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(
            data={"field_errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(methods=['patch'], detail=True, url_path='approve-task')
    def approve_task(self, request, pk):
        """
        Update a task approval status to Approved
        """
        task = self.get_object(pk)
        task.approve_task()
        return Response(
            data={"detail": [_("Task approval successful".format(pk))]},
            status=status.HTTP_202_ACCEPTED
        )

    @action(methods=['patch'], detail=True, url_path='disapprove-task')
    def disapprove_task(self, request, pk):
        """
        Disapprove a task
        """
        task = self.get_object(pk)
        task.reject_approval_request()
        return Response(data={"detail": [_("Task approval denied")]})

    @action(methods=['patch'], detail=True, url_path='start-task')
    def start_task(self, request, pk):
        """
        Start a task, Status change from pending to due
        """
        task = self.get_object(pk)
        task.start_task()
        return Response(data={"detail": [_("Task start successful")]})

    @action(methods=['patch'], detail=True, url_path='submit-task')
    def submit_task(self, request, pk):
        """
        Submit a task, Status change from due to submitted
        """
        task = self.get_object(pk)
        task.submit_task()
        return Response(data={"detail": [_("Task submission successful")]})

    @action(methods=['patch'], detail=True, url_path='accept-submission')
    def accept_task_submission(self, request, pk):
        """
        Accept a task submission, Status change from submitted to completed
        """
        task = self.get_object(pk)
        task.accept_task_submission()
        return Response(data={"detail": [_("Task submission accepted")]})

    @action(methods=['patch'], detail=True, url_path='reject-submission')
    def reject_task_submission(self, request, pk):
        """
        Reject a task submission, Status change back to due.
        """
        task = self.get_object(pk)
        task.reject_task_submission()
        return Response(data={"detail": [_("Task submission rejected")]})

    def get_permissions(self):
        permissions = []
        if self.action == 'create':
            permissions += [CanCreateTask]
        elif self.action in ['list', 'task_list_statistics']:
            permissions += [CanViewAllTasks]
        elif self.action == 'force_delete':
            permissions += [CanDeleteTask]
        elif self.action == 'retrieve':
            permissions += [IsTaskOwner|IsTaskAssignee|IsTaskParents]
        elif self.action == 'update':
            permissions += [IsTaskOwner, CanUpdateTask]
        elif self.action in ['approve_task', 'disapprove_task']:
            permissions += [HasPermissionToApproveTask]
        elif self.action in ['start_task', 'submit_task']:
            permissions += [IsTaskAssignee]
        elif self.action in ['destroy', 'accept_task_submission', 'reject_task_submission']:
            permissions += [IsTaskOwner]
        return [permission() for permission in permissions]

    def get_serializer_class(self):
        if self.action == 'task_list_statistics':
            return TaskStatusStatisticsSerializer
        return TaskSerializer


class TaskAttachmentsAdd(TemplateAPIView):
    permission_classes = [IsTaskOwner|IsTaskAssignee]
    serializer_class = TaskAttachmentsSerializer
    model = Task

    def post(self, request:Request, task_pk):
        attachment = request.FILES.get("attachment")
        task = self.get_object(pk=task_pk)
        attached_by = request.user
        task_attachment = TaskAttachments.create_factory(
            commit=True,
            attachment=attachment,
            task=task,
            attached_by=attached_by
        )
        serializer = self.serializer_class(instance=task_attachment)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class TaskAttachmentsDelete(TemplateAPIView):
    permission_classes = [IsAttachmentOwner]
    serializer_class = TaskAttachmentsSerializer
    model = TaskAttachments

    def delete(self, request:Request, task_attachment_pk):
        task_attachment = self.get_object(pk=task_attachment_pk)
        task_attachment.delete()
        return Response(
            data={"detail": [_("Attachment delete successful")]},
            status=status.HTTP_202_ACCEPTED
        )


class TaskBasedAttachments(TemplateAPIView):
    permission_classes = [IsTaskOwner|IsTaskAssignee|IsTaskParents]
    serializer_class = TaskAttachmentsSerializer
    model = Task

    def get(self, request:Request, task_pk):
        task = self.get_object(pk=task_pk)
        attachments = task.task_attachments.all()
        serializer = self.serializer_class(instance=attachments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


