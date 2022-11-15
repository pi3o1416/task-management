
from django.urls import path, include
from rest_framework import routers
from .views import MyTokenObtainPairView, MyTokenRefreshView, LogoutView, UserViewSet


user_router = routers.DefaultRouter()
user_router.register('', UserViewSet, 'user')

app_name = 'authentication'
urlpatterns = [
    path('get-token/', MyTokenObtainPairView.as_view(), name='obtain-token'),
    path('refresh-token/', MyTokenRefreshView.as_view(), name='refresh-token'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', include(user_router.urls)),
]





