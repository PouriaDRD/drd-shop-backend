from django.contrib import admin

from commerce.models import CouponUsageModel

DEV = True


@admin.register(CouponUsageModel)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = (
        "coupon",
        "wallet",
        "order",
        "discount_amount_display",
        "created_at",
    )

    list_filter = (
        "coupon",
        "created_at",
    )

    search_fields = (
        "coupon__code",
        "wallet__user__email",
        "order__id",
    )

    readonly_fields = (
        "id",
        "coupon",
        "wallet",
        "order",
        "discount_amount",
        "created_at",
    )

    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return DEV

    def has_change_permission(self, request, obj=None):
        return DEV

    def has_delete_permission(self, request, obj=None):
        return DEV

    def discount_amount_display(self, obj):
        return f"{obj.discount_amount:,}"
