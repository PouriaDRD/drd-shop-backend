from django.contrib import admin

from billing.models import CartModel

DEV = False


@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "total_price",
        "subtotal",
        "discount",
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

    def has_add_permission(self, request):
        return DEV

    def has_change_permission(self, request, obj=None):
        return DEV

    def has_delete_permission(self, request, obj=None):
        return DEV
