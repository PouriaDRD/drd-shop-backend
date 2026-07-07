from django.db import transaction

from support.models import TicketMessageModel


class TicketMessageRepository:
    """
    Database operations for ticket messages.
    """

    @staticmethod
    @transaction.atomic
    def create(
        **kwargs,
    ) -> TicketMessageModel:
        """
        Create ticket message.
        """

        return TicketMessageModel.objects.create(**kwargs)

    @staticmethod
    def get_ticket_messages(
        ticket_id,
    ):
        """
        Get all messages.
        """

        return (
            TicketMessageModel.objects.filter(
                ticket_id=ticket_id,
            )
            .select_related(
                "sender",
            )
            .order_by(
                "created_at",
            )
        )

    @staticmethod
    def get_message_by_id(
        message_id,
    ):
        return TicketMessageModel.objects.filter(
            id=message_id,
        ).first()
