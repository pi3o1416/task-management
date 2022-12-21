
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from ..serializers import (MyTokenObtainPairSerializer, MyTokenRefreshSerializer,
                           MessageSerializer, PasswordForgetSerializer,
                           PasswordResetSerializer, FieldErrorSerializer,
                           AccessTokenSerializer)
from ..models import CustomUser


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
                        httponly=True, samesite=None, secure=True)
    return response

@extend_schema(responses={200: AccessTokenSerializer,
                          401: MessageSerializer})
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
        return super().finalize_response(request, response, *args, **kwargs)


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


class LogoutView(APIView):
    permission_classes = [AllowAny,]

    @extend_schema(request=None, responses=MessageSerializer)
    def post(self, request):
        """
        Logout view. Remove refresh token from cookie
        """
        response = Response({'message': 'Logout Successful'}, status=status.HTTP_200_OK)
        response.delete_cookie("refresh_token")
        return response


class ForgetPasswordView(APIView):
    permission_classes = [AllowAny,]
    serializer_class = PasswordForgetSerializer

    @extend_schema(responses={200: MessageSerializer,
                              400: FieldErrorSerializer})
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.instance
            user.send_password_reset_email()
            return Response(data={"detail": "A Password Reset Link is send to your email."}, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    serializer_class = PasswordResetSerializer

    @extend_schema(responses={202: MessageSerializer,
                              404: MessageSerializer,
                              400: FieldErrorSerializer})
    def post(self, request, uidb64, token):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.get_user_by_encoded_pk(uidb64)
            if user and user.validate_token(token):
                serializer.get_password()
                user.set_password(serializer.get_password())
                user.save()
                return Response(data={"detail": _("Password Reset Successful")}, status=status.HTTP_202_ACCEPTED)
            return Response(data={"detail": _("Invalid URL")}, status=status.HTTP_404_NOT_FOUND)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


