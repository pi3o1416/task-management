
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission, Group
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from services.pagination import CustomPageNumberPagination
from services.views import TemplateAPIView
from authentication.permissions import IsOwner
from .queries import get_group_by_pk, get_permission_by_pk
from .serializers import (
    PermissionSerializer, GroupSerializer, GroupDetailSerializer,
    PermissionDetailSerializer, GroupAssignSerializer, GroupMinimalSerializer
)


User = get_user_model()


class GroupViewSet(ViewSet, CustomPageNumberPagination):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def create(self, request):
        """
        Group create view
        """
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
        Group list view
        """
        groups = Group.objects.all()
        page = self.paginate_queryset(queryset=groups, request=request)
        serializer = self.get_serializer_class()(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)

    def destroy(self, request, pk):
        """
        Group destroy view
        """
        group = get_group_by_pk(pk=pk)
        group.delete()
        return Response(data={"detail": [_("Group delete successful")]}, status=status.HTTP_202_ACCEPTED)

    def retrieve(self, request, pk):
        """
        Group retrieve view
        """
        group = get_group_by_pk(pk=pk)
        serializer = self.get_serializer_class()(instance=group)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        """
        Group udpate view
        """
        group = get_group_by_pk(pk=pk)
        serializer = self.get_serializer_class()(data=request.data, instance=group)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data={"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        """
        Get serializer class by action
        """
        if self.action in ['retrieve', 'list']:
            return GroupDetailSerializer
        else:
            return GroupSerializer


class PermissionViewSet(ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def list(self, request):
        """
        Permission list view
        """
        permissions = Permission.objects.all()
        serializer = self.get_serializer_class()(instance=permissions, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        """
        Permission retrieve view
        """
        permission = get_permission_by_pk(pk=pk)
        serializer = self.get_serializer_class()(instance=permission)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        """
        Get serializer class by action
        """
        if self.action in ['retrieve']:
            return PermissionDetailSerializer
        else:
            return PermissionSerializer


class AssignGroup(APIView):
    serializer_class = GroupAssignSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"detail": [_("Gropu assignment successful")]}, status=status.HTTP_201_CREATED)
        return Response(data={"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AllUserPermissions(TemplateAPIView):
    serializer_class = PermissionDetailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser|IsOwner]
    model = User

    def get(self, request, user_pk):
        user = self.get_object(pk=user_pk)
        permissions = self.get_queryset(user=user)
        serializer = self.serializer_class(instance=permissions, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self, user):
        if user.is_superuser == True:
            return Permission.objects.all()
        permission = Permission.objects.select_related('content_type').filter(group__user=user)
        return permission


class UserGroups(TemplateAPIView):
    serializer_class = GroupMinimalSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    model = User

    def get(self, request, user_pk):
        user = self.get_object(user_pk)
        user_groups = user.groups.all()
        serializer = self.serializer_class(instance=user_groups, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
















