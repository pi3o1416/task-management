
from django.urls import path, include, re_path
from rest_framework import routers
from .views import MyTokenObtainPairView, MyTokenRefreshView, LogoutView, UserViewSet, ForgetPasswordView, PasswordResetView, ActiveAccount


user_router = routers.DefaultRouter()
user_router.register('', UserViewSet, 'user')

app_name = 'authentication'
urlpatterns = [
    path('get-token/', MyTokenObtainPairView.as_view(), name='obtain-token'),
    path('refresh-token/', MyTokenRefreshView.as_view(), name='refresh-token'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forget-password/', ForgetPasswordView.as_view(), name='forget-password'),
    path('reset-password/<str:uidb64>/<str:token>', PasswordResetView.as_view(), name='reset-password'),
    path('active-account/<str:uidb64>/<str:token>', ActiveAccount.as_view(), name='active-account'),
    path('users/', include(user_router.urls)),
]





