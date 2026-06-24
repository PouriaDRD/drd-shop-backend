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
        "phone_number",
        "email",
        # permissions
        "role",
        "status",
        # dates
        "last_login",
        "updated_at",
        "created_at",
    ]

    search_fields = [
        "phone_number",
        "email",
    ]

    list_filter = [
        "role",
        "status",
    ]

    ordering = [
        "-created_at",
    ]

    readonly_fields = [
        "id",
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
                    "phone_number",
                    "email",
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
                    "phone_number",
                    "email",
                    "password",
                ),
            },
        ),
        (
            "Role & Status",
            {
                "fields": (
                    "role",
                    "status",
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
