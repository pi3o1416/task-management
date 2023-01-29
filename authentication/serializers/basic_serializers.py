
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import CustomUser


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
        fields = ['pk', 'photo', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'password', 'password2']
        read_only_fields = ['pk', 'photo', 'is_active', 'is_staff']

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise ValidationError(detail=_("Password and Retype Password did not match"), code='mismatch')
        return data

    def create(self, validated_data):
        assert validated_data, "call is_valid method before create new user"
        _ = validated_data.pop('password2')
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
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
        user = CustomUser.objects.get_user_by_email(email=email)
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


class UserPaginatedSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.URLField()
    previous = serializers.URLField()
    results = UserSerializer(many=True)


class UploadPhotoSerializer(serializers.ModelSerializer):
    photo = serializers.FileField(
        required=True
    )
    class Meta:
        model = CustomUser
        fields = ['photo']

    def validate_photo(self, image):
        if image.size > 4*1024*1024:
            raise ValidationError(detail=_("Image size should be less than 4mb"))
        return image















