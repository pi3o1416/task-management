
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

GetAuthenticatedUserDoc = Documentation(
    request=None,
    responses={
        200: OpenApiResponse(
            response=ResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Get authenticated user detail",
                    value={
                        "response_data": UserSerializer(UserFactory.build()).data,
                        "status": 200,
                        "error": None,
                    },
                    response_only=True,
                    status_codes=[200]
                )
            ]
        )
    }
)

ActiveAccountByAdminDoc = Documentation(
    request=None,
    responses={
        202: OpenApiResponse(
            response=ResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Active user account by admin",
                    value={
                        "response_data": {
                            "detail": "success_message"
                        },
                        "status": 202,
                        "error": None,
                    },
                    response_only=True,
                    status_codes=[202]
                )
            ]
        )
    }
)

DeactiveAccountByAdminDoc = Documentation(
    request=None,
    responses={
        202: OpenApiResponse(
            response=ResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Deactive user account by admin",
                    value={
                        "response_data": {
                            "detail": "success_message"
                        },
                        "status": 202,
                        "error": None,
                    },
                    response_only=True,
                    status_codes=[202]
                )
            ]
        )
    }
)

GrantStaffPermissionDoc = Documentation(
    request=None,
    responses={
        202: OpenApiResponse(
            response=ResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Grant user staff permission",
                    value={
                        "response_data": {
                            "detail": "success_message"
                        },
                        "status": 202,
                        "error": None,
                    },
                    response_only=True,
                    status_codes=[202]
                )
            ]
        )
    }
)


RemoveStaffPermissionDoc = Documentation(
    request=None,
    responses={
        202: OpenApiResponse(
            response=ResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Remove user staff permission",
                    value={
                        "response_data": {
                            "detail": "success_message"
                        },
                        "status": 202,
                        "error": None,
                    },
                    response_only=True,
                    status_codes=[202]
                )
            ]
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

UploadUserPhotoDoc = Documentation(
    responses={
        202: OpenApiResponse(
            response=ResponseSerializer,
            examples=[
                OpenApiExample(
                    name="User Account Activation Successful",
                    value={
                        "photo": "some url"
                    },
                    response_only=True,
                    status_codes=[202]
                )
            ]
        ),
    }
)

