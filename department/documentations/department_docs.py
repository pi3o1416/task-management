
from drf_spectacular.utils import OpenApiParameter

from . import Documentation
from ..serializers import (
    DepartmentSerializer, FieldErrorsSerializer,
    MessageSerializer, DepartmentPaginatedSerializer,
)


DepartmentViewSetCreateDoc = Documentation(
    responses={
        201: DepartmentSerializer,
        400: FieldErrorsSerializer
    }
)

DepartmentViewSetUpdateDoc = Documentation(
    responses={
        202: DepartmentSerializer,
        400: FieldErrorsSerializer,
        404: MessageSerializer
    }
)

DepartmentViewSetRetrieveDoc = Documentation(
    responses={
        200: DepartmentSerializer,
        404: MessageSerializer
    }
)

DepartmentViewSetDestroyDoc = Documentation(
    responses={
        200: MessageSerializer,
        400: MessageSerializer
    }
)

DepartmentViewSetListDoc = Documentation(
    responses={
        200: DepartmentPaginatedSerializer
    },
    parameters=[
        OpenApiParameter(name='page', type=int),
        OpenApiParameter(name='page_size', type=int)
    ]
)










