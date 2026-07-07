from rest_framework import serializers

from support.models import TicketAttachmentModel


class TicketAttachmentSerializer(serializers.ModelSerializer):

    class Meta:

        model = TicketAttachmentModel

        fields = (
            "id",
            "file",
            "created_at",
        )
