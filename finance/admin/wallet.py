from django.contrib import admin

from finance.models import WalletModel

DEV = True


@admin.register(WalletModel)
class WalletAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "balance_display",
        "updated_at",
        "created_at",
    )

    search_fields = ("user__email",)

    readonly_fields = (
        "id",
        # "user",
        "balance",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    list_per_page = 25

    def has_add_permission(self, request):
        return DEV

    def has_change_permission(self, request, obj=None):
        return DEV

    def has_delete_permission(self, request, obj=None):
        return DEV

    def balance_display(self, obj):
        return f"{obj.balance:,}"
