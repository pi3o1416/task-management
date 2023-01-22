
from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

class CanViewAllTasks(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.has_perm('task.can_view_all_tasks'):
            return True
        return False

