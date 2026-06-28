from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import UserModel


@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for UserModel.
    """

    list_per_page = 50

    list_display = [
        # basic information
        "email",
        "email_verified",
        # permissions
        "role",
        "status",
        # dates
        "last_login",
        "updated_at",
        "created_at",
    ]

    search_fields = [
        "email",
    ]

    list_filter = [
        "email_verified",
        "role",
        "status",
    ]

    ordering = [
        "-created_at",
    ]

    readonly_fields = [
        "id",
        "role",
        "is_superuser",
        "last_login",
        "updated_at",
        "created_at",
    ]

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "role",
                    "status",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "id",
                    "email",
                    "password",
                ),
            },
        ),
        (
            "Role & Status",
            {
                "fields": (
                    "email_verified",
                    "role",
                    "status",
                    "is_superuser",
                ),
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "last_login",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
        (
            "Permissions",
            {
                "classes": ("collapse",),
                "fields": (
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
