
from rest_framework.viewsets import ViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from ..pagination import SmallPageNumberPagination, MediumPageNumberPagination, LargePageNumberPagination
from drf_spectacular.utils import extend_schema
from ..serializers import DesignationSerializer


class DesignationViewSet(ViewSet, PageNumberPagination):
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

    def list(self, request):
        """
        List of Department Designation
        """
        serializer_class = self.get_serializer_class()
        designations = Designations.objects.all()
        page = self.paginate_queryset(queryset=designations, request=request)
        serializer = serializer_class(instance=page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        return DesignationSerializer

    def get_pagination_class(self):
        return SmallPageNumberPagination















