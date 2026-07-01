from django.contrib import admin

from finance.models import (
    RefundToWalletRequestModel,
)

from finance.enums import (
    RefundToWalletStatus,
)
from finance.services import RefundService

DEV = True


# ========================================================
# WALLET REFUND ADMIN
# ========================================================
@admin.register(RefundToWalletRequestModel)
class WalletRefundAdmin(admin.ModelAdmin):

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

    def has_add_permission(self, request):
        return DEV

    def has_change_permission(self, request, obj=None):
        return DEV

    def has_delete_permission(self, request, obj=None):
        return DEV

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
