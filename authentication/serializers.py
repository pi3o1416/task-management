
from django.utils.translation import gettext_lazy
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


class FieldErrorSerializer(serializers.Serializer):
    """
    Only for documentations
    """
    field_name = serializers.ListField()


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

    def validate_email(self, email):
        return email

    def validate_first_name(self, first_name):
        if not first_name:
            raise ValidationError(_("First name can not be empty"), code='empty-not-allowed')
        return first_name

    def validate_last_name(self, last_name):
        if not last_name:
            raise ValidationError(_("Last name can not be empty"), code="empty-not-allowed")
        return last_name

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise ValidationError(detail=_("Password and Retype Password did not match"), code='mismatch')
        return data

    class Meta:
        model=CustomUser
        fields = ['pk', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'password', 'password2']
        read_only_fields = ['pk']


class PasswordForgetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        user = CustomUser.objects.get_user(email=email)
        if user:
            self.instance = user
            return email
        raise ValidationError(detail=_("No Active Account found under this email"), code='does-not-exist')


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    retype_password = serializers.CharField(
        write_only=True,
        required=True
    )

    def get_password(self):
        """
        Only call if serializer valid
        """
        return self.validated_data.get('password')

    def validate(self, data):
        """
        Custom Validtor to ensure password and retype password same.
        """
        if data['password'] != data['retype_password']:
            raise ValidationError(
                detail=_("Password and Retype password didnot match"),
                code="data-mismatch"
            )
        return data











