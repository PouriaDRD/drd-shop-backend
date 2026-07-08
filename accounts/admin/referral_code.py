from django.contrib import admin
from django.utils.html import format_html
from accounts.models import ReferralCodeModel


@admin.register(ReferralCodeModel)
class ReferralCodeAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "user",
        "signups",
        "total_earned_display",
        "total_paid_display",
        "created_at",
    )

    search_fields = (
        "code",
        "user__email",
    )

    readonly_fields = (
        "id",
        # "code",
        "signups",
        "clicks",
        "total_earned",
        "total_paid",
        "orders",
        "created_at",
        "updated_at",
    )

    list_filter = ("created_at",)

    def total_earned_display(self, obj):

        if obj.total_earned is None:
            return "-"

        amount = f"{obj.total_earned:,.0f}"

        return format_html(
            "<span>{}</span>",
            amount,
        )

    def total_paid_display(self, obj):

        if obj.total_paid is None:
            return "-"

        amount = f"{obj.total_paid:,.0f}"

        return format_html(
            "<span>{}</span>",
            amount,
        )
