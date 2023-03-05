
from django.contrib import admin
from .models import DepartmentTask


@admin.register(DepartmentTask)
class DepartmentTaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DepartmentTask._meta.fields]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['task']
        return self.readonly_fields
        pass








