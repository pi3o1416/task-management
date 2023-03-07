
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GoalViewSet, DepartmentGoals, AddReviewView

goal_router = DefaultRouter()
goal_router.register('', GoalViewSet, 'goal')

app_name='goal'
urlpatterns = [
    path('department-goals/<int:department_pk>/', DepartmentGoals.as_view(), name="department_goals"),
    path('add-review/<int:goal_pk>/', AddReviewView.as_view(), name='add_review'),
    path('', include(goal_router.urls)),
]
