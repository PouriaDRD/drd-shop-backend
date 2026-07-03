from django.contrib import admin

from finance.models import CardModel


@admin.register(CardModel)
class CardAdmin(admin.ModelAdmin):
    list_display = (
        "owner_name",
        "owner_card_number",
        "updated_at",
        "created_at",
    )

    search_fields = (
        "owner_name",
        "owner_card_number",
    )
