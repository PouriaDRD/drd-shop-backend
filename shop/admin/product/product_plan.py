from django.contrib import admin

from shop.models import ProductPlanModel


@admin.register(ProductPlanModel)
class ProductPlanAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "product",
        "price",
        "is_available",
        "is_active",
        "updated_at",
        "created_at",
    )

    list_filter = (
        "product",
        "is_available",
        "is_active",
    )

    search_fields = (
        "title",
        "product__title",
    )

    autocomplete_fields = ("product",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
