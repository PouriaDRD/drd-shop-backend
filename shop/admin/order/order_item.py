from django.contrib import admin

from shop.models import OrderItemModel

DEV = False


class OrderItemInline(admin.TabularInline):
    model = OrderItemModel
    extra = 0
    readonly_fields = (
        "id",
        "product",
        "plan",
        "quantity",
        "price",
        "created_at",
        "updated_at",
    )


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
        "order__user__email",
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

    def has_add_permission(self, request):
        return DEV

    def has_change_permission(self, request, obj=None):
        return DEV

    def has_delete_permission(self, request, obj=None):
        return DEV
