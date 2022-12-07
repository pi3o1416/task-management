
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

    class Meta:
        model=CustomUser
        fields = ['pk', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'password', 'password2']
        read_only_fields = ['pk', 'is_active', 'is_staff']

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise ValidationError(detail=_("Password and Retype Password did not match"), code='mismatch')
        return data

    def create(self):
        assert self.validated_data, "call is_valid method before create new user"
        user = CustomUser.objects.create(
            username=self.validated_data.get('username'),
            email = self.validated_data.get('email'),
            first_name = self.validated_data.get('first_name'),
            last_name = self.validated_data.get('last_name'),
        )
        user.set_password(self.validated_data.get('password'))
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields = ['pk', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
        read_only_fields = ['pk', 'is_active', 'is_staff']

    def update(self):
        assert self.validated_data, "call is_valid method before update an user"
        assert self.instance, "initialize serializer with user instance before update"
        self.instance.username = self.validated_data.get('username')
        self.instance.email = self.validated_data.get('email')
        self.instance.first_name = self.validated_data.get('first_name')
        self.instance.last_name = self.validated_data.get('last_name')
        self.instance.save()
        return self.instance


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











