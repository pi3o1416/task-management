
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
    (None, {"fields": ("username", "password")}),
    (_("Personal info"), {"fields": ("first_name", "last_name", "email", "photo")}),
    (
        _("Permissions"),
        {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        },
    ),
    (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        ( None, {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "first_name", "last_name", "email", "is_staff", "is_active"),
            },
        ),
    )
    list_display = ("pk", "username", "email", "full_name", "is_staff", "is_active")
    list_filter = ("is_active", "is_staff",)
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )



























