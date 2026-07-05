from django.contrib import admin

from commerce.models import V2rayVPNModel


@admin.register(V2rayVPNModel)
class V2rayVPNAdmin(admin.ModelAdmin):
    list_display = (
        "order_item__order__user__email",
        "order_item",
        "subscription_link",
        "expires_at",
        "updated_at",
        "created_at",
    )

    search_fields = (
        "order_item__order__user__email",
        "order_item__product__title",
        "order_item__plan__title",
    )

    readonly_fields = (
        "id",
        "updated_at",
        "created_at",
    )
