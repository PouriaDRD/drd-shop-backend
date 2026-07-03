from django.contrib import admin

from shop.models import FeatureModel


@admin.register(FeatureModel)
class FeatureAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "title",
        "value_type",
        "created_at",
    )

    list_filter = ("value_type",)

    search_fields = (
        "title",
        "key",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
