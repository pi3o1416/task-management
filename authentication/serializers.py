
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import ValidationError

from .models import CustomUser


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_staff'] = user.is_staff
        token['is_active'] = user.is_active
        return token


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        raise InvalidToken("No valid Token found in cookie 'refresh_token'")


class MessageSerializer(serializers.Serializer):
    """
    Only used for documentations
    """
    detail = serializers.ListField()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )

    def validate_password2(self):
        if self.password != self.password2:
            raise ValidationError(_('Password and retpye password did not match'))

    class Meta:
        model=CustomUser
        fields = ['pk', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'password', 'password2']
        read_only_fields = ['pk']









