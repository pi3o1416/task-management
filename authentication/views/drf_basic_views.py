
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from services.pagination import CustomPageNumberPagination
from ..models import CustomUser
from ..serializers import UserSerializer, UserUpdateSerializer, UploadPhotoSerializer
from ..permissions import IsAnonymous, UserViewSetPermission
from ..documentations.basic_view_docs import (
    UserCreateDoc, UserListDoc, UserRetrieveDoc,
    UserDestroyDoc, UserUpdateDoc, ActiveAccountDoc
)


class UserViewSet(viewsets.ViewSet, CustomPageNumberPagination):
    queryset = CustomUser.objects.all()
    permission_classes = [UserViewSetPermission]

    @extend_schema(responses=UserCreateDoc.responses,
                   parameters=UserCreateDoc.parameters)
    def create(self, request):
        """
        Create a new User
        """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response({"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses=UserListDoc.responses,
                   parameters=UserListDoc.parameters)
    def list(self, request):
        """
        Get List of User objects
        """
        serializer_class = self.get_serializer_class()
        page = self.paginate_queryset(queryset=self.queryset, request=request)
        serializer = serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)

    @extend_schema(responses=UserRetrieveDoc.responses,
                   parameters=UserRetrieveDoc.parameters)
    def retrieve(self, request, pk):
        """
        Retrieve a object detail from database
        parameter: (int)pk
        """
        serializer_class = self.get_serializer_class()
        user = self.get_object(pk=pk)
        serializer =  serializer_class(instance=user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses=UserDestroyDoc.responses,
                   parameters=UserDestroyDoc.parameters)
    def destroy(self, request, pk):
        """
        Destroy a object from database
        parameter: (int)pk
        """
        user = self.get_object(pk=pk)
        user.delete()
        return Response(data={"detail": ["User Delete Successful"]}, status=status.HTTP_200_OK)

    @extend_schema(responses=UserUpdateDoc.responses,
                   parameters=UserUpdateDoc.parameters)
    def update(self, request, pk):
        """
        Update a user profile
        parameter: (int)pk
        """
        serializer_class = self.get_serializer_class()
        user = self.get_object(pk=pk)
        serializer = serializer_class(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.update()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data={"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["patch"], detail=True, url_path='upload-photo')
    def upload_photo(self, request, pk):
        """
        Update a user photo
        parameter: (int)pk
        """
        user = self.get_object(pk=pk)
        serializer = self.get_serializer_class()(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=None)
    @action(methods=['get'], detail=False, url_path='get-authenticated-user')
    def get_authenticated_user(self, request):
        """
        Get authenticated user
        """
        user = request.user
        serializer = self.get_serializer_class()(instance=user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=None)
    @action(methods=['patch'], detail=True, url_path='activate-account')
    def activate_account(self, request, pk):
        """
        Activate a user account
        """
        user = self.get_object(pk=pk)
        user.activate_account()
        return Response(data={"detail": _("User account activation successful")}, status=status.HTTP_202_ACCEPTED)

    @extend_schema(request=None)
    @action(methods=['patch'], detail=True, url_path='deactivate-account')
    def deactivate_account(self, request, pk):
        """
        Deactivate a user account
        """
        user = self.get_object(pk=pk)
        user.deactivate_account()
        return Response(data={"detail": _("User account deactivate successful")}, status=status.HTTP_202_ACCEPTED)

    @extend_schema(request=None)
    @action(methods=['patch'], detail=True, url_path='grant-staff-permission')
    def give_user_staff_permission(self, request, pk):
        """
        Give user staff permission
        """
        user = self.get_object(pk=pk)
        user.give_staff_permissions()
        return Response(data={"detail": _("User staff permission given")}, status=status.HTTP_202_ACCEPTED)

    @extend_schema(request=None)
    @action(methods=['patch'], detail=True, url_path='remove-staff-permission')
    def remove_user_staff_permission(self, request, pk):
        """
        Remvoe user staff permission
        """
        user = self.get_object(pk=pk)
        user.remove_staff_permissions()
        return Response(data={"detail": _("User staff permission removed")}, status=status.HTTP_202_ACCEPTED)



    def get_serializer_class(self):
        if self.action == 'update':
            return UserUpdateSerializer
        elif self.action == 'upload_photo':
            return UploadPhotoSerializer
        else:
            return UserSerializer

    def get_object(self, pk):
        user = CustomUser.objects.get_object_by_pk(pk)
        self.check_object_permissions(request=self.request, obj=user)
        return user


class ActiveAccount(APIView):
    permission_classes = [IsAnonymous]
    @extend_schema(responses=ActiveAccountDoc.responses,
                   parameters=ActiveAccountDoc.parameters)
    def get(self, request, uidb64, token):
        """
        Activate Account from unique uidb64 and token generated for user.
        URL Parameter: uidb64, token
        """
        user = self.get_object(encoded_pk=uidb64)
        if user.validate_token(token):
            user.activate_account()
            return Response(data={"detail": _("Account Acivation Successful")}, status=status.HTTP_202_ACCEPTED)
        return Response(data={"detail": _("Invalid Token")}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get_object(self, encoded_pk):
        user = CustomUser.objects.get_user_by_encoded_pk(encoded_pk)
        self.check_object_permissions(request=self.request, obj=user)
        return user





