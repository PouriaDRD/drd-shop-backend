from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models.query import QuerySet
from django.http import HttpRequest

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
        "referred_by",
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
                    "referred_by",
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
                    "referred_by",
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

    def get_queryset(self, request: HttpRequest):
        return (
            super()
            .get_queryset(request)
            .select_related("referred_by")
            .order_by("-created_at")
        )
