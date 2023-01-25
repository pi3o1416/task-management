
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework import status

from ..serializers import UsersTasksSerializers, UsersTasksDetailSerializer, UsersTasksCreateAndAssignSerializer
from ..models import UsersTasks, Task
from ..permissions import IsOwner


User = get_user_model()


class UsersTasksViewSet(ViewSet, PageNumberPagination):
    @action(methods=['post'], detail=False, url_path='')
    def assign(self, request):
        """
        Assign task to user
        """
        task = Task.objects.get_task_by_pk(request.data.get('task'))
        self.check_object_permissions(request=request, obj=task)
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
        List of all tasks
        """
        tasks = UsersTasks.objects.filter_from_query_params(request)
        page = self.paginate_queryset(queryset=tasks, request=request)
        serializer = self.get_serializer_class()(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)

    def retrieve(self, request, pk):
        """
        Detail of specific task
        """
        user_task = self.get_object(pk)
        serializer = self.get_serializer_class()(instance=user_task)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        """
        Destroy specific task assignment
        """
        user_task = self.get_object(pk)
        user_task.delete()
        return Response(data={"detail": _("User Task destroy successful")})

    def get_object(self, pk):
        user_task = UsersTasks.objects.get_user_task_by_pk(pk)
        return user_task

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action == 'assign':
            permission_classes += [IsOwner]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'assign':
            return UsersTasksSerializers
        if self.action in ['list', 'retrieve']:
            return UsersTasksDetailSerializer
        return UsersTasksSerializers


class UsersTasksCreateAndAssign(APIView):
    """
    Create a new task and assign it to a user.
    """
    serializer_class = UsersTasksCreateAndAssignSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_task = serializer.create(serializer.validated_data, user)
            serializer = UsersTasksDetailSerializer(instance=user_task)
            return Response(data={"detail": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(data={"field_errors": serializer.errors})


class UserTasksList(APIView, PageNumberPagination):
    """
    API view to get user specific task list
    """
    serializer_class = UsersTasksDetailSerializer

    def get(self, request, user_pk):
        user = User.objects.get_user_by_pk(user_pk)
        user_tasks = user.user_tasks.select_related('task')
        filtered_user_tasks = user_tasks.filter_with_task(request)
        page = self.paginate_queryset(queryset=filtered_user_tasks, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)












