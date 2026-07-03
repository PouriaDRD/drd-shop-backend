from rest_framework import serializers

from finance.models import CardModel


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardModel
        fields = (
            "id",
            "owner_name",
            "owner_card_number",
            "updated_at",
            "created_at",
        )

        read_only_fields = ["__all__"]
