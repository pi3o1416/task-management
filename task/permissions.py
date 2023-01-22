
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
    def has_object_permission(self, request, view, task:Task):
        user = request.user
        if task.created_by == user:
            return True
        return False


class HasPermissionToApproveTask(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.has_perm('task.can_approve_disapprove_task'):
            return True
        return False


class IsAssignedUponUser(BasePermission):
    def has_object_permission(self, request, view, task):
        user = request.user
        if task.task_assigned_to.assigned_to == user:
            return True
        return False





