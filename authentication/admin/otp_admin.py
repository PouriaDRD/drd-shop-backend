from django.contrib import admin
from django.utils.html import format_html

from authentication.models import OTPModel
from authentication.selectors import OTPSelector


@admin.register(OTPModel)
class OTPAdmin(admin.ModelAdmin):
    """
    Admin interface for OTP records.
    """

    list_display = (
        "phone_number",
        "code",
        "attempts",
        "remaining_attempts_display",
        "status_display",
        "is_verified",
        "is_expired",
        "expires_at",
        "created_at",
    )

    search_fields = ("phone_number",)

    list_filter = (
        "is_verified",
        "created_at",
    )

    ordering = ("-created_at",)

    date_hierarchy = "created_at"

    list_per_page = 25

    readonly_fields = (
        "id",
        "phone_number",
        "code",
        "is_verified",
        "attempts",
        "expires_at",
        "created_at",
        "status_display",
        "remaining_attempts_display",
    )

    fieldsets = (
        (
            "OTP Information",
            {
                "fields": (
                    "id",
                    "phone_number",
                    "code",
                    "is_verified",
                    "attempts",
                    "remaining_attempts_display",
                    "status_display",
                ),
            },
        ),
        (
            "Expiration",
            {
                "fields": (
                    "expires_at",
                    "created_at",
                ),
            },
        ),
    )

    actions = ("delete_expired_otps",)

    # -------------------------------------
    # Custom Fields
    # -------------------------------------

    @admin.display(description="Status")
    def status_display(self, obj):
        if obj.is_verified:
            return format_html(
                '<span style="color:{};">{}</span>',
                "#7f8c8d",
                "Verified",
            )

        if OTPSelector.is_expired(obj):
            return format_html(
                '<span style="color:{};">{}</span>',
                "#e74c3c",
                "Expired",
            )

        return format_html(
            '<span style="color:{};">{}</span>',
            "#27ae60",
            "Active",
        )

    @admin.display(description="Attempts Left")
    def remaining_attempts_display(self, obj: OTPModel):
        """
        Display remaining verification attempts.
        """

        return OTPSelector.remaining_attempts(obj)

    # -------------------------------------
    # Actions
    # -------------------------------------

    @admin.action(description="Delete expired OTPs")
    def delete_expired_otps(self, request, queryset):
        """
        Delete selected expired OTP records.
        """

        expired_otps = [otp for otp in queryset if OTPSelector.is_expired(otp)]

        deleted_count = len(expired_otps)

        for otp in expired_otps:
            otp.delete()

        self.message_user(request, f"{deleted_count} expired OTP(s) deleted.")

    # -------------------------------------
    # Permissions
    # -------------------------------------

    def has_add_permission(self, request):
        """
        Prevent manual OTP creation.
        """
        return False
