from django.db import transaction
from django.db.models import QuerySet

from support.models import TicketModel
from support.enums import TicketStatus


class TicketRepository:
    """
    Database operations for tickets.
    """

    @staticmethod
    @transaction.atomic
    def create(**kwargs) -> TicketModel:
        """
        Create new ticket.
        """

        return TicketModel.objects.create(**kwargs)

    @staticmethod
    def get_by_id(
        ticket_id,
    ) -> TicketModel | None:
        """
        Get ticket by id.
        """

        return (
            TicketModel.objects.select_related(
                "user",
            )
            .prefetch_related(
                "messages",
                "messages__sender",
            )
            .filter(id=ticket_id)
            .first()
        )

    @staticmethod
    def get_user_tickets(
        user_id,
    ) -> QuerySet[TicketModel]:
        """
        Get all user tickets.
        """

        return (
            TicketModel.objects.filter(
                user_id=user_id,
            )
            .prefetch_related(
                "messages",
            )
            .order_by(
                "-created_at",
            )
        )

    @staticmethod
    def lock(
        ticket_id,
    ) -> TicketModel:
        """
        Lock ticket row.
        """

        return TicketModel.objects.select_for_update().get(
            id=ticket_id,
        )

    @staticmethod
    @transaction.atomic
    def update_status(
        ticket: TicketModel,
        status: str,
    ) -> TicketModel:
        """
        Update ticket status.
        """

        ticket.status = status

        ticket.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return ticket

    @staticmethod
    @transaction.atomic
    def close(
        ticket: TicketModel,
    ) -> TicketModel:
        """
        Close ticket.
        """

        ticket.status = TicketStatus.CLOSED

        ticket.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return ticket
