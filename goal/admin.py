
from django.contrib import admin
from .models import Goal, GoalLastEdit, Review


@admin.register(Goal)
class GloadAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Goal._meta.fields]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Review._meta.fields]


@admin.register(GoalLastEdit)
class GoalLastEditAdmin(admin.ModelAdmin):
    list_display = [field.name for field in GoalLastEdit._meta.fields]

