from django.contrib import admin

from shop.models import CartItemModel

DEV = False


@admin.register(CartItemModel)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "cart",
        "product",
        "plan",
        "quantity",
        "unit_price",
        "total_price",
        "updated_at",
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
        "cart",
        "product",
        "plan",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return DEV

    def has_change_permission(self, request, obj=None):
        return DEV

    def has_delete_permission(self, request, obj=None):
        return DEV
