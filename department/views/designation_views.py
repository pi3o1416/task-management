
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from ..exceptions import DesignationGetException
from ..pagination import CustomPageNumberPagination
from ..serializers import DesignationSerializer, MessageSerializer, FieldErrorsSerializer, DesignationPaginatedSerializer
from ..models import Designations


class DesignationViewSet(ViewSet, CustomPageNumberPagination):
    @extend_schema(request=DesignationSerializer, responses={})
    def create(self, request):
        """
        Create New Department Designations
        """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={200: DesignationPaginatedSerializer},
                   parameters=[OpenApiParameter(name='page', type=int),
                               OpenApiParameter(name='page_size', type=int)])
    def list(self, request):
        """
        List of All Designation.
        """
        serializer_class = self.get_serializer_class()
        designations = Designations.objects.all()
        page = self.paginate_queryset(queryset=designations, request=request)
        serializer = serializer_class(instance=page, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(responses={200: DesignationSerializer,
                              404: MessageSerializer})
    def destroy(self, request, pk):
        """
        Destroy Department
        URL Parameter: Designation Primary Key(int)
        """
        try:
            designation = Designations.objects.get_designation(pk=pk)
            designation.delete()
            return Response(data={"detail": ("Designation delete successful",)}, status=status.HTTP_200_OK)
        except DesignationGetException as exception:
            return Response(data={"detail": exception.args}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(responses={200: DesignationSerializer,
                              404: MessageSerializer})
    def retrieve(self, request, pk):
        """
        Retrieve Designation Object
        URL Parameter: Designation Primary Key(int)
        """
        try:
            designation = Designations.objects.get_designation(pk=pk)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=designation)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except DesignationGetException as exception:
            return Response(data={"detail": exception.args}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(request=DesignationSerializer, responses={202: DesignationSerializer,
                                                             400: FieldErrorsSerializer,
                                                             404: MessageSerializer})
    def update(self, request, pk):
        """
        Update Designation Object
        URL Parameter: Designation Primary Key(int)
        """
        try:
            designation = Designations.objects.get_designation(pk=pk)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=designation, data=request.data)
            if serializer.is_valid():
                serializer.update()
                return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DesignationGetException as exception:
            return Response(data={"detail": exception.args}, status=status.HTTP_404_NOT_FOUND)


    def get_serializer_class(self):
        return DesignationSerializer















