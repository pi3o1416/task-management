
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GoalViewSet, DepartmentGoals, GoalCreateView

goal_router = DefaultRouter()
goal_router.register('', GoalViewSet, 'goal')

app_name='goal'
urlpatterns = [
    path('department-goals/<int:department_pk>/', DepartmentGoals.as_view(), name="department_goals"),
    path('create/<int:department_pk>/', GoalCreateView.as_view(), name='goal-create-view'),
    path('', include(goal_router.urls)),
]
