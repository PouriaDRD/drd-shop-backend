from django.contrib import admin
from django.utils.html import format_html

from finance.models import TransactionModel
from finance.enums import TransactionStatus, TransactionType
from finance.services import TransactionService

DEV = True


@admin.register(TransactionModel)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "wallet",
        "amount_display",
        "type_badge",
        "status_badge",
        "is_processed",
        "reviewed_at",
        "updated_at",
        "created_at",
    )

    search_fields = ("wallet__user__email",)

    list_filter = (
        "type",
        "status",
        "created_at",
    )

    readonly_fields = (
        "id",
        "wallet",
        # "amount",
        "type",
        # "status",
        # "is_processed",
        # "reviewed_at",
        "created_at",
        "updated_at",
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
    # AMOUNT
    # ---------------------------------------------------

    @admin.display(description="Amount", ordering="amount")
    def amount_display(self, obj):
        amount = f"{obj.amount:,.0f}"

        return format_html(
            "<span>{}</span>",
            amount,
        )

    # ---------------------------------------------------
    # TYPE BADGE
    # ---------------------------------------------------

    @admin.display(description="Type", ordering="type")
    def type_badge(self, obj):
        colors = {
            TransactionType.DEPOSIT: ("#ECFDF5", "#065F46"),
            TransactionType.PURCHASE: ("#FFF1F2", "#9F1239"),
            TransactionType.REFUND_TO_WALLET: ("#EFF6FF", "#1D4ED8"),
            TransactionType.REFUND_TO_USER: ("#F5F3FF", "#6D28D9"),
            TransactionType.WITHDRAW: ("#FFFBEB", "#92400E"),
            TransactionType.ADJUSTMENT: ("#F3F4F6", "#374151"),
        }

        bg, fg = colors.get(obj.type, ("#F3F4F6", "#374151"))

        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;border-radius:999px;font-size:11px;font-weight:600;display:inline-block;">{}</span>',
            bg,
            fg,
            obj.get_type_display(),
        )

    # ---------------------------------------------------
    # STATUS BADGE
    # ---------------------------------------------------

    @admin.display(description="Status", ordering="status")
    def status_badge(self, obj):
        colors = {
            TransactionStatus.PENDING: ("#FFFBEB", "#92400E"),
            TransactionStatus.APPROVED: ("#ECFDF5", "#065F46"),
            TransactionStatus.REJECTED: ("#FEF2F2", "#991B1B"),
            TransactionStatus.CANCELLED: ("#F3F4F6", "#374151"),
        }

        bg, fg = colors.get(obj.status, ("#F3F4F6", "#374151"))

        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;border-radius:999px;font-size:11px;font-weight:600;display:inline-block;">{}</span>',
            bg,
            fg,
            obj.get_status_display(),
        )

    # ---------------------------------------------------
    # ACTIONS
    # ---------------------------------------------------

    actions = [
        "approve_transactions",
        "reject_transactions",
    ]

    # ---------------------------------------------------
    # APPROVE
    # ---------------------------------------------------
    @admin.action(description="Approve selected transactions")
    def approve_transactions(self, request, queryset):
        try:
            updated = 0

            for tx in queryset:
                if tx.status != TransactionStatus.PENDING:
                    continue

                TransactionService.approve(tx.id)

                updated += 1

            self.message_user(request, f"{updated} transactions approved.")

        except Exception as exc:
            self.message_user(request, str(exc))

    # ---------------------------------------------------
    # REJECT
    # ---------------------------------------------------
    @admin.action(description="Reject selected transactions")
    def reject_transactions(self, request, queryset):
        try:
            updated = 0

            for tx in queryset:
                if tx.status != TransactionStatus.PENDING:
                    continue

                TransactionService.reject(tx.id)

                updated += 1

            self.message_user(request, f"{updated} transactions rejected.")

        except Exception as exc:
            self.message_user(request, str(exc))
