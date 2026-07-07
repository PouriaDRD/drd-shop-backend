from django.db import transaction
from django.core.exceptions import PermissionDenied

from support.repositories import (
    TicketRepository,
    TicketMessageRepository,
    TicketAttachmentRepository,
)


from support.enums import (
    TicketStatus,
    TicketPriority,
)


class TicketService:
    """
    Business logic for ticket system.
    """

    @staticmethod
    @transaction.atomic
    def create_ticket(
        *,
        user,
        subject,
        message,
        attachments=None,
        priority=None,
    ):

        ticket = TicketRepository.create(
            user=user,
            subject=subject,
            priority=priority,
            status=TicketStatus.OPEN,
        )

        ticket_message = TicketMessageRepository.create(
            ticket=ticket,
            sender=user,
            message=message,
            is_staff=False,
        )

        if attachments:

            for file in attachments:

                TicketAttachmentRepository.create(
                    message=ticket_message,
                    file=file,
                )

        return ticket

    @staticmethod
    def get_user_tickets(
        user,
    ):

        return TicketRepository.get_user_tickets(
            user.id,
        )

    @staticmethod
    def get_ticket(
        *,
        ticket_id,
        user,
    ):

        ticket = TicketRepository.get_by_id(
            ticket_id,
        )

        if not ticket:
            return None

        if ticket.user.id != user.id:
            raise PermissionDenied("You cannot access this ticket.")

        return ticket

    @staticmethod
    @transaction.atomic
    def reply(
        *,
        ticket_id,
        user,
        message,
        attachments=None,
    ):

        ticket = TicketRepository.lock(ticket_id)

        if ticket.user.id != user.id:
            raise PermissionDenied()

        if ticket.status == TicketStatus.CLOSED:
            raise ValueError("Ticket closed")

        ticket_message = TicketMessageRepository.create(
            ticket=ticket,
            sender=user,
            message=message,
            is_staff=False,
        )

        if attachments:

            for file in attachments:

                TicketAttachmentRepository.create(
                    message=ticket_message,
                    file=file,
                )

        return ticket_message

    @staticmethod
    @transaction.atomic
    def close(
        *,
        ticket_id,
        user,
    ):

        ticket = TicketRepository.lock(
            ticket_id,
        )

        if ticket.user.id != user.id:
            raise PermissionDenied()

        return TicketRepository.close(
            ticket,
        )
