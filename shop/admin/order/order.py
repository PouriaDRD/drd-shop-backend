from django.contrib import admin

from shop.models import OrderModel
from .order_item import OrderItemInline


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline,)

    list_display = (
        "user",
        "status",
        "total_price",
        "updated_at",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "id",
        "user__email",
    )

    autocomplete_fields = ("user",)

    readonly_fields = (
        "id",
        "updated_at",
        "created_at",
    )
