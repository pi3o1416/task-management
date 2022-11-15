
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from ..models import CustomUser
from ..serializers import MessageSerializer, UserSerializer
from ..exceptions import UserGetException


class UserViewSet(viewsets.ViewSet):
    queryset = CustomUser.objects.all()

    @extend_schema(request=UserSerializer, responses={201: UserSerializer,
                                                      400: MessageSerializer,
                                                      403: MessageSerializer})
    def create(self, request):
        """
        Create a new User
        """
        breakpoint()
        serializer = UserSerializer(data=request.POST.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=None, responses={201: UserSerializer})
    def list(self, request):
        """
        Get List of User objects
        """
        serializer = UserSerializer(instance=self.queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=None, responses={200: UserSerializer,
                                            400: MessageSerializer})
    def retrieve(self, request, pk):
        """
        Retrieve a object detail from database
        parameter: (int)pk
        """
        try:
            user = self.get_user_object(pk)
            serializer =  UserSerializer(instance=user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except UserGetException as exception:
            return Response(data={"detail": exception.args}, status=status.HTTP_400_BAD_REQUEST)

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

#    def update(self, request):
#        pass

    def get_user_object(self, pk):
        try:
            user = self.queryset.get(pk=pk)
            return user
        except CustomUser.DoesNotExist:
            raise UserGetException("User with does not found")
        except ValueError:
            raise UserGetException("User pk whold be an Integer")
        except Exception as exception:
            raise UserGetException(*exception.args)




