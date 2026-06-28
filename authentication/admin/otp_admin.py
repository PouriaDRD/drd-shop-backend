from django.contrib import admin
from django.utils.timezone import localtime

from authentication.models import OTPModel
from authentication.selectors import OTPSelector
from authentication.repositories import OTPRepository


@admin.register(OTPModel)
class OTPAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "otp_type",
        "is_used",
        "attempts",
        "remaining_attempts_display",
        "status_display",
        "expire_at_display",
        "created_at",
    )

    search_fields = ("email",)
    list_filter = ("otp_type", "is_used", "created_at")

    readonly_fields = (
        "id",
        "email",
        "otp_type",
        "salt",
        "code_hash",
        "is_used",
        "attempts",
        "created_at",
        "updated_at",
        "status_display",
        "remaining_attempts_display",
        "expire_at_display",
    )

    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_per_page = 25

    fieldsets = (
        (
            "OTP Information",
            {
                "fields": (
                    "email",
                    "otp_type",
                    "is_used",
                    "attempts",
                    "remaining_attempts_display",
                    "status_display",
                ),
            },
        ),
        (
            "Security Details",
            {
                "fields": ("salt", "code_hash"),
                "classes": ("collapse",),
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "expire_at_display",
                ),
            },
        ),
    )

    def status_display(self, obj):
        if obj.is_used:
            return "Used"
        if OTPSelector.is_expired(obj):
            return "Expired"
        return "Active"

    status_display.short_description = "Status"  # type: ignore

    def remaining_attempts_display(self, obj):
        return OTPSelector.remaining_attempts(obj) or 0

    remaining_attempts_display.short_description = "Attempts Left"  # type: ignore

    def expire_at_display(self, obj):
        value = OTPSelector.expire_at(obj)
        if not value:
            return "-"
        return localtime(value).strftime("%Y-%m-%d %H:%M:%S")

    expire_at_display.short_description = "Expires At"  # type: ignore

    actions = ["mark_as_used", "delete_expired"]

    @admin.action(description="Mark selected OTPs as used")
    def mark_as_used(self, request, queryset):
        for otp in queryset:
            OTPRepository.mark_used(otp)
        self.message_user(request, "Done")

    @admin.action(description="Delete expired OTPs")
    def delete_expired(self, request, queryset):
        for otp in queryset:
            if OTPSelector.is_expired(otp):
                otp.delete()
        self.message_user(request, "Done")

    def has_add_permission(self, request):
        return False
