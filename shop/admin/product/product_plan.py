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

    # =========================
    # ACTIONS
    # =========================

    actions = [
        "make_active",
        "make_inactive",
        "make_available",
        "make_unavailable",
    ]

    @admin.action(description="فعال کردن پلن‌های انتخاب‌شده")
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} پلن فعال شد.")

    @admin.action(description="غیرفعال کردن پلن‌های انتخاب‌شده")
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} پلن غیرفعال شد.")

    @admin.action(description="در دسترس کردن پلن‌های انتخاب‌شده")
    def make_available(self, request, queryset):
        updated = queryset.update(is_available=True)
        self.message_user(request, f"{updated} پلن در دسترس شد.")

    @admin.action(description="غیرفعال کردن دسترسی پلن‌های انتخاب‌شده")
    def make_unavailable(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(request, f"{updated} پلن از دسترس خارج شد.")
