from django.contrib import admin

from shop.models import OrderItemModel


@admin.register(OrderItemModel)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product",
        "plan",
        "quantity",
        "price",
        "created_at",
    )

    list_filter = (
        "product",
        "plan",
    )

    search_fields = (
        "order__id",
        "product__title",
        "plan__title",
    )

    autocomplete_fields = (
        "order",
        "product",
        "plan",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
