
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProjectViewSet, DepartmentProjects, ProjectAttachmentCreate, ProjectAttachmentDelete, ProjectAttachmentsList, ProjectMemberCreateView, MembersOfProjectView, ProjectMemberDeleteView


project_router = DefaultRouter()
project_router.register('', ProjectViewSet, 'project')


app_name = 'project'
urlpatterns = [
    path('department/<int:department_pk>/', DepartmentProjects.as_view(), name='department_projects'),
    path('<int:project_pk>/create-attachment/', ProjectAttachmentCreate.as_view(), name='create_attachment'),
    path('<int:project_pk>/attachments/', ProjectAttachmentsList.as_view(), name='project_attachments_list'),
    path('attachments/delete/<int:attachment_pk>/', ProjectAttachmentDelete.as_view(), name='delete_attachment'),
    path('<int:project_pk>/members-add/', ProjectMemberCreateView.as_view(), name='project_member_add'),
    path('<int:project_pk>/members/', MembersOfProjectView.as_view(), name='members_of_project'),
    path('<int:project_pk>/members/<int:user_pk>/delete/', ProjectMemberDeleteView.as_view(), name='delete_project_member'),
    path('', include(project_router.urls)),
]



