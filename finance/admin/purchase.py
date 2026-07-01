from django.contrib import admin

from finance.enums import PurchaseStatus
from finance.models import PurchaseRequestModel
from finance.services import PurchaseService

DEV = True


@admin.register(PurchaseRequestModel)
class PurchaseRequestAdmin(admin.ModelAdmin):
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
        "reviewed_at",
        "transaction",
        "is_processed",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    list_per_page = 25

    def has_delete_permission(self, request, obj=None):
        return DEV

    actions = [
        "approve_purchases",
        "reject_purchases",
    ]

    # ---------------------------------------------------
    # APPROVE
    # ---------------------------------------------------
    @admin.action(description="Approve purchases")
    def approve_purchases(self, request, queryset):
        try:
            updated = 0

            for purchase in queryset:
                if purchase.status != PurchaseStatus.PENDING:
                    continue

                PurchaseService.approve(purchase.id)

                updated += 1

            self.message_user(request, f"{updated} purchases approved.")
        except Exception as exc:
            self.message_user(request, str(exc))

    # ---------------------------------------------------
    # REJECT
    # ---------------------------------------------------
    @admin.action(description="Reject purchases")
    def reject_purchases(self, request, queryset):
        try:
            updated = 0

            for purchase in queryset:
                if purchase.status != PurchaseStatus.PENDING:
                    continue

                PurchaseService.reject(purchase.id)

                updated += 1

            self.message_user(request, f"{updated} purchases rejected.")

        except Exception as exc:
            self.message_user(request, str(exc))
