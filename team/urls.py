
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TeamViewSet


team_router = DefaultRouter()
team_router.register('', TeamViewSet, 'team')

app_name='team'
urlpatterns = [
    path('', include(team_router.urls))
]




