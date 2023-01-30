
from drf_spectacular.utils import extend_schema
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from ..models import CustomUser
from ..serializers import (MyTokenObtainPairSerializer, MyTokenRefreshSerializer,
                           PasswordForgetSerializer, PasswordResetSerializer)
from ..documentations.auth_view_docs import (
    GetTokenDoc, RefreshTokenDoc, LogoutDoc, ForgetPassswordDoc,
    PasswordResetDoc
)


def _set_cookie(response=None, cookie_name=None, cookie_value=None, max_age=3600*24*15):
    """
    Set httponly cookie in response.
    Get response, cookie_name, cookie value as parameter
    retrun response.
    """
    assert response != None, 'Response should not be null'
    assert cookie_name != None, 'Cookie Name should not be null'
    assert cookie_value != None, 'Cookie Value should not be null'
    response.set_cookie(cookie_name, cookie_value, max_age,
                        httponly=True, samesite="None", secure=True)
    return response


@extend_schema(responses=GetTokenDoc.responses,
               parameters=GetTokenDoc.parameters)
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            refresh_token = response.data.get('refresh')
            response = _set_cookie(
                response=response,
                cookie_name='refresh_token',
                cookie_value=refresh_token
            )
            del response.data['refresh']
        #Formatting Error message with desired response form
        if response.data.get('detail'):
            error_detail = response.data.get('detail')
            response.data['detail'] = [error_detail]
        if response.status_code == 400:
            response.data = {"field_errors": response.data}
        return super().finalize_response(request, response, *args, **kwargs)


@extend_schema(responses=RefreshTokenDoc.responses,
               parameters=RefreshTokenDoc.parameters)
class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer
    permission_classes = [AllowAny]

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            refresh_token = response.data.get('refresh')
            response = _set_cookie(
                response=response,
                cookie_name='refresh_token',
                cookie_value=refresh_token
            )
            del response.data['refresh']
        #Formatting Error message with desired response form
        if response.data.get('detail'):
            error_detail = response.data.get('detail')
            response.data['detail'] = [error_detail]
        return super().finalize_response(request, response, *args, **kwargs)


@extend_schema(responses=LogoutDoc.responses,
               parameters=LogoutDoc.parameters)
class LogoutView(APIView):
    permission_classes = []

    def post(self, request):
        """
        Logout view. Remove refresh token from cookie
        """
        response = Response({'detail': ['Logout Successful']}, status=status.HTTP_200_OK)
        refresh_token = RefreshToken(request.COOKIES.get('refresh_token'))
        refresh_token.blacklist()
        response.delete_cookie("refresh_token")
        del request.COOKIES['refresh_token']
        return response

@extend_schema(responses=ForgetPassswordDoc.responses,
               parameters=ForgetPassswordDoc.parameters)
class ForgetPasswordView(APIView):
    permission_classes = [AllowAny,]
    serializer_class = PasswordForgetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.instance
            user.send_password_reset_email()
            return Response(data={"detail": ["A Password Reset Link is send to your email."]}, status=status.HTTP_200_OK)
        return Response(data={"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(responses=PasswordResetDoc.responses,
               parameters=PasswordResetDoc.parameters)
class PasswordResetView(APIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.get_user_by_encoded_pk(uidb64)
            if user and user.validate_token(token):
                serializer.get_password()
                user.set_password(serializer.get_password())
                user.save()
                return Response(data={"detail": (_("Password Reset Successful"),)}, status=status.HTTP_202_ACCEPTED)
            return Response(data={"detail": (_("Invalid URL"),)}, status=status.HTTP_404_NOT_FOUND)
        return Response(data={"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


