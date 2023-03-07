
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GoalViewSet, DepartmentGoals

goal_router = DefaultRouter()
goal_router.register('', GoalViewSet, 'goal')

app_name='goal'
urlpatterns = [
    path('department-goals/<int:department_pk>/', DepartmentGoals.as_view(), name="department_goals"),
    path('', include(goal_router.urls)),
]
