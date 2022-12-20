
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


class UserViewSet(viewsets.ViewSet, CustomPageNumberPagination):
    queryset = CustomUser.objects.all()

    @extend_schema(request=UserSerializer, responses={201: UserSerializer,
                                                      400: MessageSerializer,
                                                      403: MessageSerializer})
    def create(self, request):
        """
        Create a new User
        """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        try:
            serializer_class = self.get_serializer_class()
            user = self.get_user_object(pk)
            serializer =  serializer_class(instance=user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except UserGetException as exception:
            return Response(data={"detail": exception.args}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={200: MessageSerializer,
                              400: MessageSerializer})
    def destroy(self, request, pk):
        """
        Destroy a object from database
        parameter: (int)pk
        """
        try:
            user = self.get_user_object(pk)
            user.delete()
            return Response(data={"detail": ("User Delete Successful",)}, status=status.HTTP_200_OK)
        except UserGetException as exception:
            return Response(data={"detail": exception.args}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=UserUpdateSerializer, responses={200: UserUpdateSerializer,
                                                            400: FieldErrorSerializer,
                                                            422: MessageSerializer})
    def update(self, request, pk):
        """
        Update a user profile
        parameter: (int)pk
        """
        try:
            serializer_class = self.get_serializer_class()
            user = self.get_user_object(pk)
            serializer = serializer_class(instance=user, data=request.data)
            if serializer.is_valid():
                serializer.update()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserGetException as exception:
            return Response(data={"detail": exception.args}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


    def get_serializer_class(self):
        if self.action == 'update':
            return UserUpdateSerializer
        else:
            return UserSerializer

    def get_user_object(self, pk):
        try:
            user = self.queryset.get(pk=pk)
            return user
        except CustomUser.DoesNotExist:
            raise UserGetException("User with pk={} does not found".format(pk))
        except ValueError:
            raise UserGetException("User pk whold be an Integer")
        except Exception as exception:
            raise UserGetException(*exception.args)


class ActiveAccount(APIView):
    def get(self, request, uidb64, token):
        """
        Activate Account from unique uidb64 and token generated for user.
        URL Parameter: uidb64, token
        """
        user = CustomUser.objects.get_user_by_encoded_pk(uidb64)
        if user and user.validate_token(token):
            user.activate_account()
            return Response(data={"detail": "Account Acivation Successful"}, status=status.HTTP_202_ACCEPTED)
        return Response(data={"detail": "Invalid Token or uid"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)





