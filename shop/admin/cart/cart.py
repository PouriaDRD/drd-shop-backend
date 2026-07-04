from django.contrib import admin

from shop.models import CartModel


@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "subtotal",
        "discount",
        "total_price",
        "updated_at",
        "created_at",
    )

    list_filter = ("created_at",)

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
