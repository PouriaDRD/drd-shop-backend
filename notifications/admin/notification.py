from django.contrib import admin

from notifications.models import NotificationModel


@admin.register(NotificationModel)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "notification_type",
        "is_read",
        "created_at",
    )
    list_filter = (
        "notification_type",
        "is_read",
        "created_at",
    )
    search_fields = (
        "title",
        "message",
        "user__email",
        "user__username",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)
