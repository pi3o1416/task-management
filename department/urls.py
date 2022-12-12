
from django.urls import path, include
from rest_framework import routers
from .views import DepartmentViewSet

department_router = routers.DefaultRouter()
department_router.register('', DepartmentViewSet, 'department')

app_name="department"
urlpatterns = [
    path('', include(department_router.urls)),

]
