
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import DepartmentMember
from ..serializers import DepartmentMemberSerializer, FieldErrorsSerializer, MessageSerializer, DepartmentMemberPaginatedSerializer, DepartmentMemberUpdateSerializer
from ..pagination import CustomPageNumberPagination


class DepartmentMemberViewSet(ViewSet, CustomPageNumberPagination):

    @extend_schema(responses={201: DepartmentMemberSerializer,
                              400: MessageSerializer})
    def create(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={200: DepartmentMemberPaginatedSerializer},
                   parameters=[OpenApiParameter(name='page', type=int),
                               OpenApiParameter(name='page_size', type=int),
                               OpenApiParameter(name='department_name', type=str),
                               OpenApiParameter(name='designation_title', type=str),
                               OpenApiParameter(name='member_full_name', type=str),
                               OpenApiParameter(name='department', type=int),
                               OpenApiParameter(name='member', type=int),
                               OpenApiParameter(name='designation', type=int)])
    def list(self, request):
        serializer_class = self.get_serializer_class()
        members = DepartmentMember.objects.filter_from_query_prams(request)
        page = self.paginate_queryset(queryset=members, request=request)
        serializer = serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)

    @extend_schema(responses={200: DepartmentMemberSerializer,
                              404: MessageSerializer})
    def retrieve(self, request, pk):
        serializer_class = self.get_serializer_class()
        member = DepartmentMember.objects.get_member(pk=pk)
        serializer = serializer_class(instance=member)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses={202: MessageSerializer,
                              404: MessageSerializer})
    def destroy(self, request, pk):
        member = DepartmentMember.objects.get_member(pk=pk)
        member.delete()
        return Response(data={"detail": ["Department Member Delete Successful"]}, status=status.HTTP_202_ACCEPTED)

    @extend_schema(responses={202: DepartmentMemberSerializer,
                              400: FieldErrorsSerializer,
                              404: MessageSerializer})
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

    @extend_schema(responses={200: DepartmentMemberPaginatedSerializer},
                   parameters=[OpenApiParameter(name='page', type=int),
                               OpenApiParameter(name='page_size', type=int),
                               OpenApiParameter(name='designation_title', type=str),
                               OpenApiParameter(name='member_full_name', type=str),
                               OpenApiParameter(name='member', type=int),
                               OpenApiParameter(name='designation', type=int)])
    def get(self, request, department_pk):
        department_members = DepartmentMember.objects.\
            get_members_of_department(department_pk=department_pk).\
            filter_from_query_prams(request=request)
        page = self.paginate_queryset(queryset=department_members, request=request)
        serializer = DepartmentMemberSerializer(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)












