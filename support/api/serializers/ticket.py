from rest_framework import serializers
from django.core.exceptions import ValidationError


from .ticket_message import TicketMessageSerializer

from support.models import TicketModel
from support.enums import TicketCategory
from support.services import TicketService

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def validate_file_size(file):
    if file.size > MAX_FILE_SIZE:
        raise ValidationError("حجم هر فایل نباید بیشتر از 10 مگابایت باشد.")

    return file


class TicketAttachmentField(serializers.FileField):

    def __init__(self, **kwargs):
        super().__init__(
            validators=[
                validate_file_size,
            ],
            **kwargs,
        )


class TicketCreateSerializer(serializers.Serializer):

    title = serializers.CharField()

    message = serializers.CharField()

    category = serializers.ChoiceField(
        choices=TicketCategory.choices,
        default=TicketCategory.GENERAL,
    )

    attachments = serializers.ListField(
        child=TicketAttachmentField(),
        required=False,
        max_length=5,
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
            "category",
            "status",
            "updated_at",
            "created_at",
        )

        read_only_fields = ["__all__"]


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
        child=TicketAttachmentField(),
        required=False,
        max_length=5,
    )

    def create(self, validated_data):

        request = self.context["request"]

        ticket_id = self.context["ticket_id"]

        return TicketService.reply(
            ticket_id=ticket_id,
            user=request.user,
            **validated_data,
        )
