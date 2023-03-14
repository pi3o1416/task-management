
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    DepartmentTaskAssign, DepartmentTaskCreateAssign, UserAssignedToDepartmentTaskList,
    AuthUserAssignedToDepartmentTasksList, DepartmentTaskOperationsViewSet, AllDepartmentTaskList,
    AuthUserDepartmentTasksList
)


dept_task_operations = DefaultRouter()
dept_task_operations.register('operations', DepartmentTaskOperationsViewSet, 'dept_task_operations')


app_name='department_task'
urlpatterns = [
    path('assign/<int:task_pk>/', DepartmentTaskAssign.as_view(), name='assign'),
    path('assign-and-create/', DepartmentTaskCreateAssign.as_view(), name='create_assign'),
    path('user/<int:user_pk>/assigned-to-department-tasks/', UserAssignedToDepartmentTaskList.as_view(), name='assigned_to_tasks'),
    path('auth-user/assigned-to-department-tasks/', AuthUserAssignedToDepartmentTasksList.as_view(), name='auth-user-assigned-to-tasks'),
    path('auth-user/tasks-of-department', AuthUserDepartmentTasksList.as_view(), name='auth-user-tasks-of-department'),
    path('all-tasks/', AllDepartmentTaskList.as_view(), name='department-tasks'),
    path('', include(dept_task_operations.urls)),
]
