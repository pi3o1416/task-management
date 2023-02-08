
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProjectViewSet


project_router = DefaultRouter()
project_router.register('', ProjectViewSet, 'project')


app_name = 'project'
urlpatterns = [
    path('', include(project_router.urls)),
]



