
from django.contrib import admin
from .models import Designations, Department, DepartmentMember


@admin.register(Designations)
class DesignationsAdmin(admin.ModelAdmin):
    list_display = ["pk", "department", "title"]
    pass


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "slug", "description"]


@admin.register(DepartmentMember)
class DepartmentMemberAdmin(admin.ModelAdmin):
    list_display = ["pk", "member", "department", "designation", "is_head"]








