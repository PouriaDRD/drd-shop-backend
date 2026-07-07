from rest_framework import serializers

from support.models import TicketModel

from .ticket_message import TicketMessageSerializer

from support.enums import TicketCategory
from support.services import TicketService


class TicketCreateSerializer(serializers.Serializer):

    title = serializers.CharField()

    message = serializers.CharField()

    category = serializers.ChoiceField(
        choices=TicketCategory.choices,
        default=TicketCategory.GENERAL,
    )

    attachments = serializers.ListField(
        child=serializers.FileField(),
        required=False,
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
            "title",
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
            "title",
            "status",
            "messages",
            "updated_at",
            "created_at",
        )


class TicketReplySerializer(serializers.Serializer):

    message = serializers.CharField(
        min_length=1,
    )

    attachments = serializers.ListField(
        child=serializers.FileField(),
        required=False,
    )

    def create(self, validated_data):

        request = self.context["request"]

        ticket_id = self.context["ticket_id"]

        return TicketService.reply(
            ticket_id=ticket_id,
            user=request.user,
            **validated_data,
        )
