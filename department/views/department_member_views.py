
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import DepartmentMember
from ..serializers import DepartmentMemberSerializer, DepartmentMemberUpdateSerializer
from ..pagination import CustomPageNumberPagination
from ..documentations import department_member_docs as docs


class DepartmentMemberViewSet(ViewSet, CustomPageNumberPagination):

    @extend_schema(
        responses=docs.DepartmentMemberCreateDoc.responses,
        parameters=docs.DepartmentMemberCreateDoc.parameters
    )
    def create(self, request):
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
        serializer_class = self.get_serializer_class()
        members = DepartmentMember.objects.filter_from_query_prams(request)
        page = self.paginate_queryset(queryset=members, request=request)
        serializer = serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)

    @extend_schema(
        responses=docs.DepartmentMemberRetrieve.responses,
        parameters=docs.DepartmentMemberRetrieve.parameters
    )
    def retrieve(self, request, pk):
        serializer_class = self.get_serializer_class()
        member = DepartmentMember.objects.get_member(pk=pk)
        serializer = serializer_class(instance=member)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses=docs.DepartmentMemberDestroyDoc.responses,
        parameters=docs.DepartmentMemberDestroyDoc.parameters
    )
    def destroy(self, request, pk):
        member = DepartmentMember.objects.get_member(pk=pk)
        member.delete()
        return Response(data={"detail": ["Department Member Delete Successful"]}, status=status.HTTP_202_ACCEPTED)

    @extend_schema(
        responses=docs.DepartmentMemberUpdateDoc.responses,
        parameters=docs.DepartmentMemberUpdateDoc.parameters
    )
    def update(self, request, pk):
        member = DepartmentMember.objects.get_member(pk=pk)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=member, data=request.data)
        if serializer.is_valid():
            serializer.update(instance=member, validated_data=serializer.validated_data)
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == 'update':
            return DepartmentMemberUpdateSerializer
        return DepartmentMemberSerializer


class MembersOfDepartmentView(APIView, CustomPageNumberPagination):

    @extend_schema(
        responses=docs.MembersOfDepartmentDoc.responses,
        parameters=docs.MembersOfDepartmentDoc.parameters
    )
    def get(self, request, department_pk):
        department_members = DepartmentMember.objects.\
            get_members_of_department(department_pk=department_pk).\
            filter_from_query_prams(request=request)
        page = self.paginate_queryset(queryset=department_members, request=request)
        serializer = DepartmentMemberSerializer(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)












