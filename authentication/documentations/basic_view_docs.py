
from rest_framework import serializers
from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from . import Documentation
from ..serializers import ResponseSerializer
from ..serializers.basic_serializers import UserSerializer
from ..factories import UserFactory


UserViewSetCreateDoc = Documentation(
    responses={
        201: OpenApiResponse(
            response=ResponseSerializer,
            examples=[
                OpenApiExample(
                    name="User Create successful",
                    value={
                        "data":UserSerializer(UserFactory.build()).data,
                        "status":201,
                        "error":None,
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            response=ResponseSerializer,
            examples=[
                OpenApiExample(
                    name="User Create bad request",
                    value={
                        "data":UserSerializer(UserFactory.build()).data,
                        "status":201,
                        "error":None,
                    }
                )
            ]
        ),
    }
)

UserViewSetUpdateDoc = Documentation(
    responses={

    }
)

UserViewSetDestroyDoc = Documentation(
    responses={

    }
)

UserViewSetRetrieveDoc = Documentation(
    responses={

    }
)

UserViewSetListDoc = Documentation(
    responses={

    }
)

ActiveAccountDoc = Documentation(
    responses={

    }
)

