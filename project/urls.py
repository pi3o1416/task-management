
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProjectViewSet, DepartmentProjects


project_router = DefaultRouter()
project_router.register('', ProjectViewSet, 'project')


app_name = 'project'
urlpatterns = [
    path('department/<int:department_pk>/', DepartmentProjects.as_view(), name='department_projects'),
    path('', include(project_router.urls)),
]



