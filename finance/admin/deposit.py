from django.contrib import admin

from finance.enums import DepositStatus
from finance.services import DepositService
from finance.models import DepositRequestModel

DEV = True


@admin.register(DepositRequestModel)
class DepositRequestAdmin(admin.ModelAdmin):
    list_display = (
        "amount",
        "payment_method",
        "status",
        "transaction",
        "is_processed",
        "reviewed_at",
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

    def has_delete_permission(self, request, obj=None):
        return DEV

    actions = [
        "approve_deposits",
        "reject_deposits",
    ]

    # ---------------------------------------------------
    # APPROVE
    # ---------------------------------------------------
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

    # ---------------------------------------------------
    # REJECT
    # ---------------------------------------------------
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
