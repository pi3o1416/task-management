
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GoalViewSet

goal_router = DefaultRouter()
goal_router.register('', GoalViewSet, 'goal')

app_name='goal'
urlpatterns = [
    path('goals/', include(goal_router.urls)),
]
