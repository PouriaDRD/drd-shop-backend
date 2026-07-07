from rest_framework import serializers

from support.models import TicketMessageModel
from .ticket_attachment import TicketAttachmentSerializer


class TicketMessageSerializer(serializers.ModelSerializer):

    sender = serializers.CharField(
        source="sender.email",
        read_only=True,
    )

    attachments = TicketAttachmentSerializer(
        many=True,
        read_only=True,
    )

    class Meta:

        model = TicketMessageModel

        fields = (
            "id",
            "sender",
            "message",
            "is_staff",
            "attachments",
            "created_at",
        )
