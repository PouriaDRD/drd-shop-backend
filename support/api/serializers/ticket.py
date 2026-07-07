from rest_framework import serializers

from support.models import TicketModel

from .ticket_message import TicketMessageSerializer

from support.services.ticket import TicketService


class TicketCreateSerializer(serializers.Serializer):
    """
    Create ticket serializer.
    """

    subject = serializers.CharField(
        max_length=255,
        required=True,
    )

    message = serializers.CharField(
        required=True,
        min_length=5,
    )

    def create(self, validated_data):

        request = self.context["request"]

        return TicketService.create_ticket(
            user=request.user,
            **validated_data,
        )


class TicketListSerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketModel

        fields = (
            "id",
            "subject",
            "status",
            "updated_at",
            "created_at",
        )


class TicketDetailSerializer(serializers.ModelSerializer):

    messages = TicketMessageSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = TicketModel

        fields = (
            "id",
            "subject",
            "status",
            "messages",
            "updated_at",
            "created_at",
        )


class TicketReplySerializer(serializers.Serializer):

    message = serializers.CharField(
        min_length=1,
    )

    def create(self, validated_data):

        request = self.context["request"]

        ticket_id = self.context["ticket_id"]

        return TicketService.reply(
            ticket_id=ticket_id,
            user=request.user,
            message=validated_data["message"],
        )
