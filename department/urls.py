
from django.urls import path, include
from rest_framework import routers
from .views import DesignationViewSet, DepartmentDesignationsView, DepartmentViewSet, DepartmentMemberViewSet, MembersOfDepartmentView

department_router = routers.DefaultRouter()
department_router.register('', DepartmentViewSet, 'department')

designation_router = routers.DefaultRouter()
designation_router.register('', DesignationViewSet, 'designation')

department_member_router = routers.DefaultRouter()
department_member_router.register('', DepartmentMemberViewSet, 'members')

app_name="department"
urlpatterns = [
    path('designations/', include(designation_router.urls)),
    path('members/', include(department_member_router.urls)),
    path('<int:department_pk>/designations/', DepartmentDesignationsView.as_view(), name="department-designations"),
    path('<int:department_pk>/department-members/', MembersOfDepartmentView.as_view(), name='members-of-department'),
    path('', include(department_router.urls)),
]
