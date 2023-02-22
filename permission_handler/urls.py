
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PermissionViewSet, GroupViewSet, AssignGroup, AllUserPermissions, UserGroups, RemoveFromGroup


permission_router = DefaultRouter()
permission_router.register('', PermissionViewSet, 'permission')

group_router = DefaultRouter()
group_router.register('', GroupViewSet, 'group')

app_name='permission_handler'
urlpatterns = [
    path('permissions/', include(permission_router.urls)),
    path('groups/<int:group_pk>/remove-user/<int:user_pk>/', RemoveFromGroup.as_view(), name='remove_from_group'),
    path('groups/', include(group_router.urls)),
    path('assign-group/', AssignGroup.as_view(), name='assign_group'),
    path('user/<int:user_pk>/user-permissions/', AllUserPermissions.as_view(), name='user_permissions'),
    path('user/<int:user_pk>/user-groups/', UserGroups.as_view(), name='user_groups'),
]






