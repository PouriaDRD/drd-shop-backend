from django.contrib import admin

from finance.models import TransactionModel
from finance.enums import TransactionStatus
from finance.services import TransactionService

DEV = True


@admin.register(TransactionModel)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "wallet",
        "type",
        "amount",
        "status",
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
        "amount",
        "type",
        "description",
        "status",
        "is_processed",
        "reviewed_at",
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
                if tx.status == TransactionStatus.APPROVED:
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
                if tx.status == TransactionStatus.REJECTED:
                    continue

                TransactionService.reject(tx.id)

                updated += 1

            self.message_user(request, f"{updated} transactions rejected.")

        except Exception as exc:
            self.message_user(request, str(exc))
