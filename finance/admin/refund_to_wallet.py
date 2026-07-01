from django.contrib import admin

from finance.models import RefundToWalletRequestModel


@admin.register(RefundToWalletRequestModel)
class RefundToWalletRequestAdmin(admin.ModelAdmin):
    list_display = (
        "amount",
        "status",
        "transaction",
        "is_processed",
        "reviewed_at",
        "created_at",
    )

    search_fields = ("transaction__wallet__user__email",)

    list_filter = (
        "status",
        "created_at",
    )

    readonly_fields = (
        "id",
        "status",
        "transaction",
        "is_processed",
        "reviewed_at",
        "updated_at",
        "created_at",
    )

    ordering = ("-created_at",)

    list_per_page = 25
