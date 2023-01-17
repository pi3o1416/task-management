
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PermissionViewSet, GroupViewSet, AssignGroup, AllUserPermissions


permission_router = DefaultRouter()
permission_router.register('', PermissionViewSet, 'permission')

group_router = DefaultRouter()
group_router.register('', GroupViewSet, 'group')

app_name='permission_handler'
urlpatterns = [
    path('permissions/', include(permission_router.urls)),
    path('groups/', include(group_router.urls)),
    path('assign-group/', AssignGroup.as_view(), name='assign-group'),
    path('user-permissions/<int:user_pk>/', AllUserPermissions.as_view(), name='user-permissions'),
]






