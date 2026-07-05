from django.contrib import admin

from commerce.models import ProductModel


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "slug",
        "title",
        "type",
        "is_active",
        "updated_at",
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

    # =========================
    # ACTIONS
    # =========================

    actions = ["make_active", "make_inactive"]

    @admin.action()
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} activated")

    @admin.action()
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} deactivated")
