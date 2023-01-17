
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PermissionViewSet


permission_router = DefaultRouter()
permission_router.register('', PermissionViewSet, 'permission')

app_name='permission_handler'
urlpatterns = [
    path('permission/', include(permission_router.urls)),

]






