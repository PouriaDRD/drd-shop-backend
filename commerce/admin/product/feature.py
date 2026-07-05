from django.contrib import admin

from commerce.models import FeatureModel


@admin.register(FeatureModel)
class FeatureAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "title",
        "value_type",
        "updated_at",
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
