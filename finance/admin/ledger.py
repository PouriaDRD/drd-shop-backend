from django.contrib import admin

from finance.models import LedgerEntryModel

DEV = True


@admin.register(LedgerEntryModel)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = (
        "wallet",
        "transaction",
        "transaction_type",
        "amount",
        "balance_before",
        "balance_after",
        "created_at",
    )

    search_fields = ("wallet__user__email",)

    list_filter = (
        "transaction_type",
        "created_at",
    )

    readonly_fields = (
        "id",
        "transaction",
        "wallet",
        "transaction_type",
        "amount",
        "balance_before",
        "balance_after",
        "created_at",
    )

    ordering = ("-created_at",)

    list_per_page = 25

    def has_add_permission(self, request):
        return DEV

    def has_change_permission(self, request, obj=None):
        return DEV

    def has_delete_permission(self, request, obj=None):
        return DEV
