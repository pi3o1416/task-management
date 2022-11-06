
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from ..serializers import MyTokenObtainPairSerializer, MyTokenRefreshSerializer


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
        return super().finalize_response(request, response, *args, **kwargs)


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer
    permission_classes = [IsAuthenticated]

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            refresh_token = response.data.get('refresh')
            response = _set_cookie(
                response=response,
                cookie_name='refresh_token',
                cookie_value=refresh_token
            )
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)


class LogoutView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        """
        Logout view. Remove refresh token from cookie
        """
        response = Response({'message': 'Logout Successful'}, status=status.HTTP_200_OK)
        response.delete_cookie("refresh_tokne")
        return response
