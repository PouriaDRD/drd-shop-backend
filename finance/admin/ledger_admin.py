from django.contrib import admin
from django.utils.html import format_html
from finance.models import LedgerEntryModel


@admin.register(LedgerEntryModel)
class LedgerAdmin(admin.ModelAdmin):

    list_display = (
        "wallet",
        "transaction_short",
        "amount_formatted",
        "created_at",
    )

    list_filter = (
        "amount",
        "created_at",
    )

    search_fields = (
        "wallet__user__phone_number",
        "transaction__id",
    )

    readonly_fields = (
        "id",
        "created_at",
    )

    ordering = ("-created_at",)

    def short_id(self, obj):
        return str(obj.id)[:8]

    short_id.short_description = "ID"  # type: ignore

    def transaction_short(self, obj):
        if not obj.transaction:
            return "-"
        return str(obj.transaction.id)[:8]

    transaction_short.short_description = "Transaction"  # type: ignore

    def amount_formatted(self, obj):
        if obj.amount is None:
            return "-"

        try:
            amount = int(obj.amount)
        except Exception:
            return obj.amount

        parts = f"{amount:,}".split(",")

        grouped = []
        for i in range(0, len(parts), 3):
            grouped.append(",".join(parts[i : i + 3]))

        formatted = " / ".join(grouped)

        return format_html(
            '<span style="color:#fbbf24;font-weight:700;">{}</span>',
            formatted,
        )

    amount_formatted.short_description = "Amount"  # type: ignore
