from django.contrib import admin

from shop.models import PlanFeatureModel


@admin.register(PlanFeatureModel)
class PlanFeatureAdmin(admin.ModelAdmin):
    list_display = (
        "plan",
        "feature",
        "value",
        "created_at",
    )

    list_filter = (
        "feature",
        "plan__product",
    )

    search_fields = (
        "plan__title",
        "feature__title",
        "value",
    )

    autocomplete_fields = (
        "plan",
        "feature",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
