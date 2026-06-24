from django.contrib import admin
from django.utils.html import format_html
from finance.models import WalletModel
from finance.repositories import WalletRepository


@admin.register(WalletModel)
class WalletAdmin(admin.ModelAdmin):

    list_per_page = 20

    list_display = (
        "user",
        "balance_formatted",
        "updated_at",
        "created_at",
    )

    search_fields = (
        "user__id",
        "user__phone_number",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "get_balance",
    )

    def short_id(self, obj):
        return str(obj.id)[:8]

    short_id.short_description = "ID"  # type: ignore

    def get_balance(self, obj):
        return WalletRepository.get_balance(obj)

    get_balance.short_description = "Balance"  # type: ignore

    def balance_formatted(self, obj):
        balance = WalletRepository.get_balance(obj)

        if balance is None:
            return "-"

        try:
            balance = int(balance)
        except Exception:
            return balance

        parts = f"{balance:,}".split(",")

        grouped = []
        for i in range(0, len(parts), 3):
            grouped.append(",".join(parts[i : i + 3]))

        formatted = " / ".join(grouped)

        return format_html(
            '<span style="color:#fbbf24;font-weight:700;">{}</span>',
            formatted,
        )

    balance_formatted.short_description = "Balance"  # type: ignore
