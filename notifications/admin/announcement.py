from django.contrib import admin

from notifications.models import AnnouncementModel


@admin.register(AnnouncementModel)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "type",
        "is_active",
        "is_pinned",
        "starts_at",
        "expires_at",
        "created_at",
    )
    list_filter = (
        "type",
        "is_active",
        "is_pinned",
    )
    search_fields = (
        "title",
        "description",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    ordering = ("-is_pinned", "-created_at")
