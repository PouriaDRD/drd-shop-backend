from django.contrib import admin

from shop.models import ProductModel


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "slug",
        "title",
        "type",
        "is_active",
        "created_at",
    )

    list_filter = (
        "type",
        "is_active",
    )

    search_fields = (
        "title",
        "slug",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    prepopulated_fields = {
        "slug": ("title",),
    }

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "title",
                    "slug",
                    "description",
                    "type",
                    "is_active",
                )
            },
        ),
        (
            "Dates",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
