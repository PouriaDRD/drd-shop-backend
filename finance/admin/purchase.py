from django.contrib import admin
from django.utils.html import format_html

from finance.enums import PurchaseStatus
from finance.models import PurchaseRequestModel
from finance.services import PurchaseService

DEV = False


@admin.register(PurchaseRequestModel)
class PurchaseRequestAdmin(admin.ModelAdmin):
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
        "reviewed_at",
        "transaction",
        "is_processed",
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
            PurchaseStatus.PENDING: ("#FFFBEB", "#92400E"),
            PurchaseStatus.APPROVED: ("#ECFDF5", "#065F46"),
            PurchaseStatus.REJECTED: ("#FEF2F2", "#991B1B"),
            PurchaseStatus.CANCELLED: ("#F3F4F6", "#374151"),
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
