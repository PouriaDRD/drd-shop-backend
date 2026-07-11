from django.db import transaction
from django.db.models import Prefetch, QuerySet

from support.enums import TicketStatus
from support.models import TicketModel, TicketMessageModel, TicketAttachmentModel


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
        Return all tickets for a user with messages and attachments prefetched.
        """

        return (
            TicketModel.objects.filter(
                user_id=user_id,
            )
            .prefetch_related(
                Prefetch(
                    "messages",
                    queryset=(
                        TicketMessageModel.objects.select_related("sender")
                        .prefetch_related(
                            Prefetch(
                                "attachments",
                                queryset=TicketAttachmentModel.objects.only(
                                    "id",
                                    "message_id",
                                    "file",
                                    "created_at",
                                ),
                            )
                        )
                        .order_by("created_at")
                    ),
                )
            )
            .order_by("-created_at")
        )

    @staticmethod
    def get_all_tickets() -> QuerySet[TicketModel]:
        """
        Return all tickets.
        """

        return TicketModel.objects.select_related("user").prefetch_related(
            Prefetch(
                "messages",
                queryset=TicketMessageModel.objects.order_by("created_at"),
            )
        )

    @staticmethod
    def get_admin_ticket(ticket_id: str):
        return (
            TicketModel.objects.select_related("user")
            .prefetch_related(
                Prefetch(
                    "messages",
                    queryset=(
                        TicketMessageModel.objects.select_related("sender")
                        .prefetch_related(
                            Prefetch(
                                "attachments",
                                queryset=TicketAttachmentModel.objects.only(
                                    "id",
                                    "message_id",
                                    "file",
                                    "created_at",
                                ),
                            )
                        )
                        .order_by("created_at")
                    ),
                )
            )
            .get(id=ticket_id)
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
