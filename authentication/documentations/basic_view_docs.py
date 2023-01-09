
from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from . import Documentation, ResponseSerializer
from ..serializers.basic_serializers import UserSerializer
from ..factories import UserFactory



UserCreateDoc = Documentation(
    responses={
        201: OpenApiResponse(
            response=ResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Created",
                    value={
                        "response_data":UserSerializer(UserFactory.build()).data,
                        "status":201,
                        "error":None,
                    },
                    response_only=True
                )
            ]
        ),
    }
)


UserListDoc = Documentation(
    responses={
        200: OpenApiResponse(
            response=ResponseSerializer,
            examples=[
                OpenApiExample(
                    name="User List",
                    value={
                        "response_data":UserSerializer(
                            [UserFactory.build()],
                            many=True
                        ).data,
                        "status":200,
                        "error":None,
                    },
                    response_only=True
                )
            ]
        )
    }
)

UserDestroyDoc = Documentation(
    responses={
        200: OpenApiResponse(
            response=ResponseSerializer,
            examples=[
                OpenApiExample(
                    name="User Delete Successful",
                    value={
                        "response_data":{
                            "detail": ["success_message"]
                        },
                        "status":200,
                        "error":None,
                    },
                    response_only=True
                )
            ]
        )
    }
)

UserRetrieveDoc = Documentation(
    responses={
        200: OpenApiResponse(
            response=ResponseSerializer,
            examples=[
                OpenApiExample(
                    name="User Retrieve Successful",
                    value={
                        "response_data":UserSerializer(UserFactory.build()).data,
                        "status":200,
                        "error":None,
                    },
                    response_only=True
                )
            ]
        )
    }
)

UserUpdateDoc = Documentation(
    responses={
        202: OpenApiResponse(
            response=ResponseSerializer,
            examples=[
                OpenApiExample(
                    name="User Update Successful",
                    value={
                        "response_data":UserSerializer(UserFactory.build()).data,
                        "status":202,
                        "error":None,
                    },
                    response_only=True,
                    status_codes=[202]
                )
            ],
        )
    }
)

ActiveAccountDoc = Documentation(
    responses={
        202: OpenApiResponse(
            response=ResponseSerializer,
            examples=[
                OpenApiExample(
                    name="User Account Activation Successful",
                    value={
                        "response_data":{
                            "detail": ["success_message"]
                        },
                        "status":202,
                        "error":None,
                    },
                    response_only=True,
                    status_codes=[202]
                )
            ]
        ),
    }
)

