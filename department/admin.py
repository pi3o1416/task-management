
from django.contrib import admin
from .models import Designations, Department, DepartmentMember


@admin.register(Designations)
class DesignationsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Designations._meta.fields]


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Department._meta.fields]


@admin.register(DepartmentMember)
class DepartmentMemberAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DepartmentMember._meta.fields]








