
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, UsersTasksViewSet, UsersTasksCreateAndAssign, UserTasksList, TaskAttachmentsAdd


task_router = DefaultRouter()
task_router.register('', TaskViewSet, 'task')

users_tasks_router = DefaultRouter()
users_tasks_router.register('', UsersTasksViewSet, 'users-tasks')


app_name='task'
urlpatterns = [
    path('users-tasks/', include(users_tasks_router.urls)),
    path('user/<int:user_pk>/', UserTasksList.as_view(), name='user-tasks-list'),
    path('user-task-create/', UsersTasksCreateAndAssign.as_view(), name='user_task_create'),
    path('<int:task_pk>/add-attachment/', TaskAttachmentsAdd.as_view(), name='attach-file'),
    path('', include(task_router.urls)),
]

