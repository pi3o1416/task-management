
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProjectViewSet, DepartmentProjects, ProjectAttachmentCreate, ProjectAttachmentDelete, ProjectAttachmentsList


project_router = DefaultRouter()
project_router.register('', ProjectViewSet, 'project')


app_name = 'project'
urlpatterns = [
    path('department/<int:department_pk>/', DepartmentProjects.as_view(), name='department_projects'),
    path('<int:project_pk>/create-attachment/', ProjectAttachmentCreate.as_view(), name='create_attachment'),
    path('<int:project_pk>/attachments/', ProjectAttachmentsList.as_view(), name='project_attachments_list'),
    path('attachments/delete/<int:attachment_pk>/', ProjectAttachmentDelete.as_view(), name='delete_attachment'),
    path('', include(project_router.urls)),
]



