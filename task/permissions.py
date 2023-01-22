
from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission
from .models import Task

class CanViewAllTasks(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.has_perm('task.can_view_all_tasks'):
            return True
        return False


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj:Task):
        user = request.user
        if obj.created_by == user:
            return True
        return False

