
from drf_spectacular.utils import OpenApiParameter

from . import Documentation
from ..serializers import (
    DepartmentMemberSerializer, FieldErrorsSerializer,
    MessageSerializer, DepartmentMemberPaginatedSerializer,
)

DepartmentMemberCreateDoc = Documentation(
    responses={
        201: DepartmentMemberSerializer,
        400: MessageSerializer
    }
)

DepartmentMemberListDoc = Documentation(
    responses={
        200: DepartmentMemberPaginatedSerializer
    },
    parameters=[
        OpenApiParameter(name='page', type=int),
        OpenApiParameter(name='page_size', type=int),
        OpenApiParameter(name='department_name', type=str),
        OpenApiParameter(name='designation_title', type=str),
        OpenApiParameter(name='member_full_name', type=str),
        OpenApiParameter(name='department', type=int),
        OpenApiParameter(name='member', type=int),
        OpenApiParameter(name='designation', type=int)
    ]
)

DepartmentMemberUpdateDoc = Documentation(
    responses={
        202: DepartmentMemberSerializer,
        400: FieldErrorsSerializer,
        404: MessageSerializer}
)

DepartmentMemberDestroyDoc = Documentation(
    responses={
        202: MessageSerializer,
        404: MessageSerializer
    }
)

DepartmentMemberRetrieve = Documentation(
    responses={
        200: DepartmentMemberSerializer,
        404: MessageSerializer
    }
)

MembersOfDepartmentDoc = Documentation(
    responses={
        200: DepartmentMemberPaginatedSerializer
    },
    parameters=[
        OpenApiParameter(name='page', type=int),
        OpenApiParameter(name='page_size', type=int),
        OpenApiParameter(name='designation_title', type=str),
        OpenApiParameter(name='member_full_name', type=str),
        OpenApiParameter(name='member', type=int),
        OpenApiParameter(name='designation', type=int)
    ]
)


