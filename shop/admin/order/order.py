from django.contrib import admin

from shop.models import OrderModel


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "total_price",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "id",
        "user__email",
        "user__phone_number",
    )

    autocomplete_fields = ("user",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
