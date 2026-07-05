from django.contrib import admin
from django.utils.html import format_html

from finance.models import RefundToWalletRequestModel
from finance.enums import RefundToWalletStatus
from finance.services import RefundService

DEV = True


@admin.register(RefundToWalletRequestModel)
class WalletRefundAdmin(admin.ModelAdmin):

    list_display = (
        "wallet__user__email",
        "amount_display",
        "status_badge",
        "transaction",
        "is_processed",
        "reviewed_at",
        "updated_at",
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
    # STATUS BADGE
    # ---------------------------------------------------

    @admin.display(description="Status", ordering="status")
    def status_badge(self, obj):
        colors = {
            RefundToWalletStatus.PENDING: ("#FFFBEB", "#92400E"),
            RefundToWalletStatus.APPROVED: ("#ECFDF5", "#065F46"),
            RefundToWalletStatus.REJECTED: ("#FEF2F2", "#991B1B"),
            RefundToWalletStatus.CANCELLED: ("#F3F4F6", "#374151"),
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

    actions = ["approve", "reject"]

    @admin.action(description="Approve wallet refunds")
    def approve(self, request, queryset):
        try:
            updated = 0

            for obj in queryset:
                if obj.status != RefundToWalletStatus.PENDING:
                    continue

                RefundService.approve_wallet_refund(obj.id)
                updated += 1

            self.message_user(request, f"{updated} wallet refunds approved.")

        except Exception as e:
            self.message_user(request, f"Error approving refunds: {str(e)}")

    @admin.action(description="Reject wallet refunds")
    def reject(self, request, queryset):
        try:
            updated = 0

            for obj in queryset:
                if obj.status != RefundToWalletStatus.PENDING:
                    continue

                RefundService.reject_wallet_refund(
                    refund_id=obj.id, note="Rejected by admin"
                )
                updated += 1

            self.message_user(request, f"{updated} wallet refunds rejected.")

        except Exception as e:
            self.message_user(request, f"Error rejecting refunds: {str(e)}")
