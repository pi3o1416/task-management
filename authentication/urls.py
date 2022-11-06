
from django.urls import path
from .views.drf_auth_views import MyTokenObtainPairView, MyTokenRefreshView, LogoutView

app_name = 'authentication'
urlpatterns = [
    path('get-token/', MyTokenObtainPairView.as_view(), name='obtain-token'),
    path('refresh-token/', MyTokenRefreshView.as_view(), name='refresh-token'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

