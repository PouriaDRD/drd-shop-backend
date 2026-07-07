from rest_framework import serializers

from support.models import TicketMessageModel


class TicketMessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(
        source="sender.email",
        read_only=True,
    )

    class Meta:
        model = TicketMessageModel

        fields = (
            "id",
            "sender",
            "message",
            "is_staff",
            "created_at",
        )
        read_only_fields = ["__all__"]
