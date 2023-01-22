
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet


task_router = DefaultRouter()
task_router.register('', TaskViewSet, 'task')


app_name='task'
urlpatterns = [
    path('', include(task_router.urls))
]

