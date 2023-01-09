
from drf_spectacular.utils import OpenApiExample, OpenApiResponse
from . import Documentation, ResponseSerializer


GetTokenDoc = Documentation(
    responses={
        200: OpenApiResponse(
            response=ResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Token obtain successful",
                    value={
                        "response_data": {
                            "access": "access_token"
                        },
                        "status": 200,
                        "error": None
                    },
                    status_codes=[200]
                )
            ]
        )
    }
)


RefreshTokenDoc = Documentation(
    responses={
        200: OpenApiResponse(
            response=ResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Token Refresh successful",
                    value={
                        "response_data": {
                            "access": "access_token"
                        },
                        "status": 200,
                        "error": None
                    },
                    status_codes=[200]
                )
            ]
        )
    }
)


LogoutDoc = Documentation(
    responses={
        200: OpenApiResponse(
            response=ResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Logout successful",
                    value={
                        "response_data": {
                            "detail": "Logout Successful"
                        },
                        "status": 200,
                        "error": None
                    },
                    status_codes=[200]
                )
            ]
        )
    }
)


ForgetPassswordDoc = Documentation(
    responses={
        200: OpenApiResponse(
            response=ResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Logout successful",
                    value={
                        "response_data": {
                            "detail": "Password Reset email sent"
                        },
                        "status": 200,
                        "error": None
                    },
                    status_codes=[200]
                )
            ]
        )
    }
)


PasswordResetDoc = Documentation(
    responses={
        202: OpenApiResponse(
            response=ResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Password reset successful",
                    value={
                        "response_data": {
                            "detail": "Password Reset Successful"
                        },
                        "status": 202,
                        "error": None
                    },
                    status_codes=[202]
                )
            ]
        )
    }
)



