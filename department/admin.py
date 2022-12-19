
from django.contrib import admin
from .models import Designations, Department, DepartmentMember


@admin.register(Designations)
class DesignationsAdmin(admin.ModelAdmin):
    pass


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass


@admin.register(DepartmentMember)
class DepartmentMemberAdmin(admin.ModelAdmin):
    pass







