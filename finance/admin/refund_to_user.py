from django.contrib import admin
from django.utils.html import format_html

from finance.models import RefundToUserRequestModel
from finance.services.refund import RefundService
from finance.enums import RefundToUserStatus

DEV = True


@admin.register(RefundToUserRequestModel)
class UserRefundAdmin(admin.ModelAdmin):

    list_display = (
        "wallet__user__email",
        "receiver_name",
        "amount_display",
        "status_badge",
        "transaction",
        "is_processed",
        "reviewed_at",
        "updated_at",
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
            RefundToUserStatus.PENDING: ("#FFFBEB", "#92400E"),
            RefundToUserStatus.APPROVED: ("#ECFDF5", "#065F46"),
            RefundToUserStatus.REJECTED: ("#FEF2F2", "#991B1B"),
            RefundToUserStatus.CANCELLED: ("#F3F4F6", "#374151"),
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
