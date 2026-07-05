from django.contrib import admin
from django.utils.html import format_html

from finance.enums import DepositStatus, DepositPaymentMethod
from finance.models import DepositRequestModel
from finance.services import DepositService

DEV = False


@admin.register(DepositRequestModel)
class DepositRequestAdmin(admin.ModelAdmin):
    list_display = (
        "wallet__user__email",
        "amount_display",
        "payment_method_badge",
        "status_badge",
        "transaction",
        "is_processed",
        "reviewed_at",
        "updated_at",
        "created_at",
    )

    search_fields = (
        "transaction__wallet__user__email",
        "tracking_code",
        "reference_number",
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

    def has_add_permission(self, request):
        return DEV

    def has_change_permission(self, request, obj=None):
        return DEV

    def has_delete_permission(self, request, obj=None):
        return DEV

    @admin.display(description="Amount", ordering="amount")
    def amount_display(self, obj):
        amount = f"{obj.amount:,.0f}"

        return format_html(
            "<span>{}</span>",
            amount,
        )

    # ------------------------------------------------------------------
    # BADGES
    # ------------------------------------------------------------------

    @admin.display(description="Status", ordering="status")
    def status_badge(self, obj):
        colors = {
            DepositStatus.PENDING: ("#FEF3C7", "#92400E"),
            DepositStatus.APPROVED: ("#DCFCE7", "#166534"),
            DepositStatus.REJECTED: ("#FEE2E2", "#991B1B"),
            DepositStatus.CANCELLED: ("#F3F4F6", "#4B5563"),
        }

        bg, fg = colors.get(obj.status, ("#F3F4F6", "#374151"))

        return format_html(
            """
            <span style="
                background:{};
                color:{};
                padding:4px 10px;
                border-radius:999px;
                font-size:11px;
                font-weight:600;
                display:inline-block;
                line-height:1.2;
            ">
                {}
            </span>
            """,
            bg,
            fg,
            obj.get_status_display(),
        )

    @admin.display(description="Payment", ordering="payment_method")
    def payment_method_badge(self, obj):
        colors = {
            DepositPaymentMethod.CARD_TO_CARD: ("#DBEAFE", "#1D4ED8"),
            DepositPaymentMethod.ONLINE_GATEWAY: ("#EDE9FE", "#6D28D9"),
        }

        bg, fg = colors.get(obj.payment_method, ("#F3F4F6", "#374151"))

        return format_html(
            """
            <span style="
                background:{};
                color:{};
                padding:4px 10px;
                border-radius:999px;
                font-size:11px;
                font-weight:600;
                display:inline-block;
                line-height:1.2;
            ">
                {}
            </span>
            """,
            bg,
            fg,
            obj.get_payment_method_display(),
        )

    # ------------------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------------------

    actions = [
        "approve_deposits",
        "reject_deposits",
    ]

    @admin.action(description="Approve deposits")
    def approve_deposits(self, request, queryset):
        try:
            updated = 0

            for deposit in queryset:
                if deposit.status != DepositStatus.PENDING:
                    continue

                DepositService.approve(deposit.id)
                updated += 1

            self.message_user(request, f"{updated} deposits approved.")

        except Exception as exc:
            self.message_user(request, str(exc))

    @admin.action(description="Reject deposits")
    def reject_deposits(self, request, queryset):
        try:
            updated = 0

            for deposit in queryset:
                if deposit.status != DepositStatus.PENDING:
                    continue

                DepositService.reject(deposit.id)
                updated += 1

            self.message_user(request, f"{updated} deposits rejected.")

        except Exception as exc:
            self.message_user(request, str(exc))
