
from django.urls import path, include
from rest_framework import routers
from .views import DepartmentViewSet
from .views import DesignationViewSet

department_router = routers.DefaultRouter()
department_router.register('', DepartmentViewSet, 'department')

designation_router = routers.DefaultRouter()
designation_router.register('', DesignationViewSet, 'designation')

app_name="department"
urlpatterns = [
    path('designations/', include(designation_router.urls)),
    path('', include(department_router.urls)),
]
