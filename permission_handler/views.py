
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission, Group
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from authentication.models import CustomUser
from .serializers import PermissionSerializer, GroupSerializer, GroupDetailSerializer, PermissionDetailSerializer, GroupAssignSerializer
from .queries import get_group_by_pk, get_permission_by_pk


class GroupViewSet(ViewSet, PageNumberPagination):
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
        serializer = self.get_serializer_class()(instance=groups, many=True)
        serializer = self.get_serializer_class()(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)

    def destroy(self, request, pk):
        """
        Group destroy view
        """
        group = get_group_by_pk(pk)
        group.delete()
        return Response(data={"detail": [_("Group delete successful")]}, status=status.HTTP_202_ACCEPTED)

    def retrieve(self, request, pk):
        """
        Group retrieve view
        """
        group = get_group_by_pk(pk)
        serializer = self.get_serializer_class()(instance=group)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        """
        Group udpate view
        """
        group = get_group_by_pk(pk)
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


class PermissionViewSet(ViewSet, PageNumberPagination):
    def list(self, request):
        """
        Permission list view
        """
        permissions = Permission.objects.all()
        page = self.paginate_queryset(queryset=permissions, request=request)
        serializer = self.get_serializer_class()(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)

    def retrieve(self, request, pk):
        """
        Permission retrieve view
        """
        permission = get_permission_by_pk(pk)
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
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"detail": [_("Gropu assignment successful")]}, status=status.HTTP_201_CREATED)
        return Response(data={"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AllUserPermissions(APIView):
    serializer_class = GroupDetailSerializer
    def get(self, request, user_pk):
        user = CustomUser.objects.get_user_by_pk(pk=user_pk)
        serializer = self.serializer_class(instance=user.groups, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)














