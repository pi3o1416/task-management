
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response

from services.pagination import CustomPageNumberPagination
from services.views import TemplateAPIView, TemplateViewSet

from ..models import DepartmentMember, Department
from ..serializers import DepartmentMemberSerializer, DepartmentMemberUpdateSerializer, DepartmentMemberDetailSerializer
from ..documentations import department_member_docs as docs


class DepartmentMemberViewSet(TemplateViewSet, CustomPageNumberPagination):
    permission_classes = [DjangoModelPermissions]
    queryset = DepartmentMember.objects.all()
    model = DepartmentMember

    @extend_schema(
        responses=docs.DepartmentMemberCreateDoc.responses,
        parameters=docs.DepartmentMemberCreateDoc.parameters
    )
    def create(self, request):
        """
        Create a department member
        """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses=docs.DepartmentMemberListDoc.responses,
        parameters=docs.DepartmentMemberListDoc.parameters
    )
    def list(self, request):
        """
        List of departments members
        """
        serializer_class = self.get_serializer_class()
        members = DepartmentMember.objects.filter_from_query_params(request)
        page = self.paginate_queryset(queryset=members, request=request)
        serializer = serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)

    @extend_schema(
        responses=docs.DepartmentMemberRetrieve.responses,
        parameters=docs.DepartmentMemberRetrieve.parameters
    )
    def retrieve(self, request, pk):
        """
        Detail of department members
        """
        serializer_class = self.get_serializer_class()
        member = self.get_object(pk=pk)
        serializer = serializer_class(instance=member)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses=docs.DepartmentMemberDestroyDoc.responses,
        parameters=docs.DepartmentMemberDestroyDoc.parameters
    )
    def destroy(self, request, pk):
        """
        Remove a department member
        """
        member = self.get_object(pk=pk)
        member.delete()
        return Response(data={"detail": ["Department Member Delete Successful"]}, status=status.HTTP_202_ACCEPTED)

    @extend_schema(
        responses=docs.DepartmentMemberUpdateDoc.responses,
        parameters=docs.DepartmentMemberUpdateDoc.parameters
    )
    def update(self, request, pk):
        """
        Update a department member
        """
        member = self.get_object(pk=pk)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=member, data=request.data)
        if serializer.is_valid():
            serializer.update()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == 'create':
            return DepartmentMemberSerializer
        if self.action == 'update':
            return DepartmentMemberUpdateSerializer
        return DepartmentMemberDetailSerializer


class MembersOfDepartmentView(TemplateAPIView, CustomPageNumberPagination):
    permission_classes = [IsAuthenticated]
    serializer_class = DepartmentMemberDetailSerializer
    model = Department

    @extend_schema(
        responses=docs.MembersOfDepartmentDoc.responses,
        parameters=docs.MembersOfDepartmentDoc.parameters
    )
    def get(self, request, department_pk):
        """
        Members of a department
        """
        department = self.get_object(pk=department_pk)
        department_members = department.department_members.select_related('member')\
            .filter_from_query_params(request=request)
        page = self.paginate_queryset(queryset=department_members, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)












