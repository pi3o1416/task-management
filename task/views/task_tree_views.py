
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework import status

from services.views import TemplateAPIView
from ..permissions import IsTaskOwner, IsTaskAssignee
from ..serializers import SubTaskCreateSerializer, TaskTreeDetailSerializer, TaskSerializer, TaskStatusStatisticsSerializer
from ..models import Task, TaskTree


class CreateSubTask(TemplateAPIView):
    model = Task
    serializer_class = SubTaskCreateSerializer
    permission_classes = [IsTaskAssignee]

    def post(self, request, task_pk):
        user = request.user
        parent_task = self.get_object(pk=task_pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            tree_edge = serializer.create(created_by=user, parent_task=parent_task, commit=True)
            response_serializer = TaskTreeDetailSerializer(instance=tree_edge)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetSubTasks(TemplateAPIView):
    model = Task
    serializer_class = TaskSerializer
    permission_classes = [IsTaskOwner, IsTaskAssignee]

    def get(self, request, task_pk):
        task = self.get_object(pk=task_pk)
        subquery = TaskTree.objects.values('child').filter(parent=task)
        subtasks = Task.objects.filter(pk__in=subquery)
        serializer = self.serializer_class(instance=subtasks, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class TaskSubTasksStats(TemplateAPIView):
    model = Task
    serializer_class = TaskStatusStatisticsSerializer

    def get(self, request, task_pk):
        task = self.get_object(pk=task_pk)
        subtasks = task.child_tasks
        subtasks_stats = subtasks.get_task_status_statistics()
        return Response(data=subtasks_stats, status=status.HTTP_200_OK)










