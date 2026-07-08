from django.contrib import admin

from accounts.models import ReferralCodeModel


@admin.register(ReferralCodeModel)
class ReferralCodeAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "user",
        "signups",
        "total_earned",
        "total_paid",
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
