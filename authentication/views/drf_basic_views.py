
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter

from authentication.serializers.basic_serializers import UserPaginatedSerializer
from ..models import CustomUser
from ..serializers import FieldErrorSerializer, MessageSerializer, UserSerializer, UserUpdateSerializer
from ..exceptions import UserGetException
from ..pagination import CustomPageNumberPagination
from ..documentations.basic_view_docs import UserViewSetCreateDoc


class UserViewSet(viewsets.ViewSet, CustomPageNumberPagination):
    queryset = CustomUser.objects.all()

    @extend_schema(responses=UserViewSetCreateDoc.responses)
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

    @extend_schema(responses={200: UserPaginatedSerializer},
                   parameters=[OpenApiParameter(name='page', type=int),
                               OpenApiParameter(name='page_size', type=int)])
    def list(self, request):
        """
        Get List of User objects
        """
        serializer_class = self.get_serializer_class()
        page = self.paginate_queryset(queryset=self.queryset, request=request)
        serializer = serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)

    @extend_schema(request=None, responses={200: UserSerializer,
                                            400: MessageSerializer})
    def retrieve(self, request, pk):
        """
        Retrieve a object detail from database
        parameter: (int)pk
        """
        serializer_class = self.get_serializer_class()
        user = CustomUser.objects.get_user_by_pk(pk)
        serializer =  serializer_class(instance=user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses={200: MessageSerializer,
                              400: MessageSerializer})
    def destroy(self, request, pk):
        """
        Destroy a object from database
        parameter: (int)pk
        """
        user = CustomUser.objects.get_user_by_pk(pk)
        user.delete()
        return Response(data={"detail": ["User Delete Successful"]}, status=status.HTTP_200_OK)

    @extend_schema(request=UserUpdateSerializer, responses={200: UserUpdateSerializer,
                                                            400: FieldErrorSerializer,
                                                            422: MessageSerializer})
    def update(self, request, pk):
        """
        Update a user profile
        parameter: (int)pk
        """
        serializer_class = self.get_serializer_class()
        user = CustomUser.objects.get_user_by_pk(pk)
        serializer = serializer_class(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.update()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data={"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def get_serializer_class(self):
        if self.action == 'update':
            return UserUpdateSerializer
        else:
            return UserSerializer


class ActiveAccount(APIView):
    @extend_schema(request=None, responses={202: MessageSerializer,
                                            422: MessageSerializer})
    def get(self, request, uidb64, token):
        """
        Activate Account from unique uidb64 and token generated for user.
        URL Parameter: uidb64, token
        """
        user = CustomUser.objects.get_user_by_encoded_pk(uidb64)
        if user.validate_token(token):
            user.activate_account()
            return Response(data={"detail": ["Account Acivation Successful"]}, status=status.HTTP_202_ACCEPTED)
        return Response(data={"detail": ["Invalid Token"]}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)





