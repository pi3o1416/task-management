
from rest_framework.request import Request
from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserViewSetPermission(BasePermission):
    def has_permission(self, request:Request, view):
        admin_only_views = ['destroy', 'activate_account', 'deactivate_account'
                            'give_user_staff_permission', 'remove_user_staff_permission']
        if view.action == 'create':
            return request.user.is_anonymous
        elif view.action in admin_only_views:
            return request.user.is_authenticated and request.user.is_staff
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action == 'update':
            return request.user == obj
        if view.action == 'upload_photo':
            return request.user == obj
        return True



class IsAnonymous(BasePermission):
    def has_permission(self, request:Request, view):
        if request.method in SAFE_METHODS:
            if request.user.is_anonymous:
                return True
        return False


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj:
            return True
        return False




