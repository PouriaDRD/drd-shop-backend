from django.contrib import admin

from shop.models import CouponModel


@admin.register(CouponModel)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "title",
        "discount_type",
        "discount_value",
        "minimum_order_amount",
        "usage_limit",
        "used_count",
        "per_user_limit",
        "is_active",
        "starts_at",
        "expires_at",
    )

    list_filter = (
        "discount_type",
        "is_active",
        "starts_at",
        "expires_at",
    )

    search_fields = (
        "code",
        "title",
    )

    filter_horizontal = ("allowed_products",)

    readonly_fields = (
        "id",
        "used_count",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "General",
            {
                "fields": (
                    "id",
                    "code",
                    "title",
                    "description",
                )
            },
        ),
        (
            "Discount",
            {
                "fields": (
                    "discount_type",
                    "discount_value",
                    "max_discount",
                    "minimum_order_amount",
                )
            },
        ),
        (
            "Availability",
            {
                "fields": (
                    "allowed_products",
                    "usage_limit",
                    "per_user_limit",
                    "used_count",
                )
            },
        ),
        (
            "Validity",
            {
                "fields": (
                    "starts_at",
                    "expires_at",
                    "is_active",
                )
            },
        ),
        (
            "Timestamps",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
