from django.contrib import admin
from django.utils.html import format_html

from finance.models import LedgerEntryModel

DEV = True


@admin.register(LedgerEntryModel)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = (
        "wallet",
        "amount_display",
        "transaction",
        "transaction_type_badge",
        "balance_before_display",
        "balance_after_display",
        "created_at",
    )

    search_fields = ("wallet__user__email",)

    list_filter = (
        "transaction_type",
        "created_at",
    )

    readonly_fields = (
        "id",
        "transaction",
        "wallet",
        "transaction_type",
        "amount",
        "balance_before",
        "balance_after",
        "created_at",
    )

    ordering = ("-created_at",)
    list_per_page = 25

    def has_add_permission(self, request):
        return DEV

    def has_change_permission(self, request, obj=None):
        return DEV

    def has_delete_permission(self, request, obj=None):
        return DEV

    # ---------------------------------------------------
    # TYPE BADGE (new minimal colors)
    # ---------------------------------------------------

    @admin.display(description="Type", ordering="transaction_type")
    def transaction_type_badge(self, obj):
        colors = {
            "deposit": ("#ECFDF5", "#065F46"),  # green soft
            "purchase": ("#FFF1F2", "#9F1239"),  # rose
            "refund_to_wallet": ("#EFF6FF", "#1D4ED8"),  # blue
            "refund_to_user": ("#F5F3FF", "#6D28D9"),  # violet
            "withdraw": ("#FFFBEB", "#92400E"),  # amber
            "adjustment": ("#F3F4F6", "#374151"),  # neutral
        }

        bg, fg = colors.get(obj.transaction_type, ("#F3F4F6", "#374151"))

        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;border-radius:999px;font-size:11px;font-weight:600;display:inline-block;">{}</span>',
            bg,
            fg,
            obj.get_transaction_type_display(),
        )

    # ---------------------------------------------------
    # AMOUNT (green if +, red if -)
    # ---------------------------------------------------

    @admin.display(description="Amount", ordering="amount")
    def amount_display(self, obj):
        amount = float(obj.amount)

        if amount < 0:
            color = "#DC2626"  # red
        else:
            color = "#16A34A"  # green

        formatted = "{:,.0f}".format(abs(amount))

        sign = "-" if amount < 0 else ""

        return format_html(
            '<span style="color:{};font-weight:700;">{}{}</span>',
            color,
            sign,
            formatted,
        )

    # ---------------------------------------------------
    # BALANCES (minimal gray style)
    # ---------------------------------------------------

    @admin.display(description="Before", ordering="balance_before")
    def balance_before_display(self, obj):
        value = "{:,.0f}".format(float(obj.balance_before))

        return format_html(
            "<span>{}</span>",
            value,
        )

    @admin.display(description="After", ordering="balance_after")
    def balance_after_display(self, obj):
        value = "{:,.0f}".format(float(obj.balance_after))

        return format_html(
            "<span>{}</span>",
            value,
        )
