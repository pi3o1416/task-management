
from drf_spectacular.utils import OpenApiParameter
from ..serializers import (
    DesignationSerializer, MessageSerializer,
    FieldErrorsSerializer, DesignationPaginatedSerializer
)

from . import Documentation


DesignationViewSetCreateDoc = Documentation(
    responses={
        201: DesignationSerializer,
        400: FieldErrorsSerializer
    }
)

DesignationViewSetUpdateDoc = Documentation(
    responses={
        202: DesignationSerializer,
        400: FieldErrorsSerializer,
        404: MessageSerializer
    }
)

DesignationViewSetDestroyDoc = Documentation(
    responses={
        200: MessageSerializer,
        404: MessageSerializer
    }
)

DesignationViewSetRetrieveDoc = Documentation(
    responses={
        200: DesignationSerializer,
        404: MessageSerializer
    }
)

DesignationViewSetListDoc = Documentation(
    responses={
        200: DesignationPaginatedSerializer
    },
    parameters=[
        OpenApiParameter(name='page', type=int),
        OpenApiParameter(name='page_size', type=int)
    ]
)

DepartmentDesignationsDoc = Documentation(
    responses={
        200: DesignationPaginatedSerializer
    },
    parameters=[
        OpenApiParameter(name='page', type=int),
        OpenApiParameter(name='page_size', type=int)
    ]
)












