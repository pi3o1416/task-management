
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    DepartmentTaskAssign, DepartmentTaskCreateAssign, AssignedOnDepartmentTaskList,
    AssignedToDepartmentTaskList, AuthUserAssignedToDepartmentTasks, DepartmentTaskOperationsViewSet
)

dept_task_operations = DefaultRouter()
dept_task_operations.register('operations', DepartmentTaskOperationsViewSet, 'dept_task_operations')



app_name='department_task'
urlpatterns = [
    path('assign/', DepartmentTaskAssign.as_view(), name='assign'),
    path('assign-and-create/', DepartmentTaskCreateAssign.as_view(), name='create_assign'),
    path('assigned-on-tasks/<int:department_pk>', AssignedOnDepartmentTaskList.as_view(), name='assigned_on_tasks'),
    path('user/<int:user_pk>/assigned-to-department-tasks/', AssignedToDepartmentTaskList.as_view(), name='assigned_to_tasks'),
    path('auth-user/assigned-to-department-tasks/', AuthUserAssignedToDepartmentTasks.as_view(), name='auth-user-assigned-to-tasks'),
    path('', include(dept_task_operations.urls))
]
