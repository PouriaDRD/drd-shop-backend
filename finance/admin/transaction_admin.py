from django.contrib import admin
from django.utils.html import format_html

from finance.models import TransactionModel
from .actions import (
    approve_deposit,
    reject_deposit,
    refund_transaction,
)


@admin.register(TransactionModel)
class TransactionAdmin(admin.ModelAdmin):
    actions = [
        approve_deposit,
        reject_deposit,
        refund_transaction,
    ]

    list_display = (
        "wallet",
        "amount_formatted",
        "status_badge",
        "transaction_type_badge",
        "payment_method_badge",
        "description",
        "updated_at",
        "created_at",
    )

    list_filter = (
        "transaction_type",
        "status",
        "created_at",
    )

    search_fields = (
        "id",
        "wallet__user__username",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    def short_id(self, obj):
        return str(obj.id)[:8]

    short_id.short_description = "ID"  # type: ignore

    def amount_formatted(self, obj):
        if obj.amount is None:
            return "-"

        try:
            amount = int(obj.amount)
        except Exception:
            return obj.amount

        return format_html(
            """
            <span style="
                color:#fbbf24;
                font-weight:700;
                font-size:13px;
            ">
                {}
            </span>
            """,
            f"{amount:,}",
        )

    amount_formatted.short_description = "Amount"  # type: ignore

    def _badge(self, text, color):
        return format_html(
            """
            <span style="
                background:{}15;
                color:{};
                border:1px solid {}35;
                padding:2px 7px;
                border-radius:5px;
                font-size:10px;
                font-weight:600;
                line-height:1.2;
                display:inline-block;
                white-space:nowrap;
            ">
                {}
            </span>
            """,
            color,
            color,
            color,
            text,
        )

    def status_badge(self, obj):
        badges = {
            "pending": ("Pending", "#f59e0b"),
            "completed": ("Completed", "#22c55e"),
            "approved": ("Approved", "#3b82f6"),
            "rejected": ("Rejected", "#ef4444"),
            "failed": ("Failed", "#dc2626"),
            "canceled": ("Canceled", "#6b7280"),
        }

        text, color = badges.get(
            obj.status,
            (obj.status.title(), "#6b7280"),
        )

        return self._badge(text, color)

    status_badge.short_description = "Status"  # type: ignore

    def transaction_type_badge(self, obj):
        badges = {
            "deposit": ("Deposit", "#22c55e"),
            "withdraw": ("Withdraw", "#e73a3a"),
            "purchase": ("Purchase", "#3b82f6"),
            "refund": ("Refund", "#f59e0b"),
        }

        text, color = badges.get(
            obj.transaction_type,
            (obj.transaction_type.title(), "#6b7280"),
        )

        return self._badge(text, color)

    transaction_type_badge.short_description = "Type"  # type: ignore

    def payment_method_badge(self, obj):
        badges = {
            "card_to_card": ("Card To Card", "#6366f1"),
            "gateway": ("Gateway", "#14b8a6"),
            "crypto": ("Crypto", "#f97316"),
            "admin": ("Admin", "#8b5cf6"),
        }

        text, color = badges.get(
            obj.payment_method,
            (obj.payment_method.replace("_", " ").title(), "#6b7280"),
        )

        return self._badge(text, color)

    payment_method_badge.short_description = "Payment Method"  # type: ignore
