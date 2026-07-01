from django.contrib import admin

from finance.models import (
    RefundToUserRequestModel,
)

from finance.services.refund import RefundService
from finance.enums import (
    RefundToUserStatus,
)

DEV = True


# ========================================================
# USER REFUND ADMIN
# ========================================================
@admin.register(RefundToUserRequestModel)
class UserRefundAdmin(admin.ModelAdmin):

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

    def has_delete_permission(self, request, obj=None):
        return DEV

    actions = ["approve", "reject"]

    @admin.action(description="Approve user refunds")
    def approve(self, request, queryset):
        try:
            updated = 0

            for obj in queryset:
                if obj.status != RefundToUserStatus.PENDING:
                    continue

                RefundService.approve_user_refund(obj.id)

                updated += 1

            self.message_user(request, f"{updated} user refunds approved.")

        except Exception as e:
            self.message_user(request, f"Error approving refunds: {str(e)}")

    @admin.action(description="Reject user refunds")
    def reject(self, request, queryset):
        try:
            updated = 0

            for obj in queryset:
                if obj.status != RefundToUserStatus.PENDING:
                    continue

                RefundService.reject_user_refund(obj.id)

                updated += 1

            self.message_user(request, f"{updated} user refunds rejected.")

        except Exception as e:
            self.message_user(request, f"Error rejecting refunds: {str(e)}")
