from django.contrib import admin

from finance.models import RefundToUserRequestModel


@admin.register(RefundToUserRequestModel)
class RefundToUserRequestAdmin(admin.ModelAdmin):
    list_display = (
        "receiver_name",
        "receiver_card_number",
        "amount",
        "status",
        "transaction",
        "is_processed",
        "reviewed_at",
        "created_at",
    )

    search_fields = (
        "transaction__wallet__user__email",
        "receiver_name",
        "receiver_card_number",
    )

    list_filter = (
        "status",
        "payment_method",
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
