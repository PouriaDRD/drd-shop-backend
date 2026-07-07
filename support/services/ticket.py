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
    TicketCategory,
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
        title,
        message,
        attachments=None,
        category=TicketCategory.GENERAL,
        priority=TicketPriority.MEDIUM,
    ):

        ticket = TicketRepository.create(
            user=user,
            title=title,
            priority=priority,
            category=category,
            status=TicketStatus.OPEN,
        )

        ticket_message = TicketMessageRepository.create(
            ticket=ticket,
            sender=user,
            message=message,
            is_staff_reply=False,
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
            is_staff_reply=False,
        )

        if attachments:

            for file in attachments:

                TicketAttachmentRepository.create(
                    message=ticket_message,
                    file=file,
                )

        TicketRepository.update_status(
            ticket,
            status=TicketStatus.OPEN,
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

    @staticmethod
    @transaction.atomic
    def staff_reply(
        *,
        message_id,
    ):
        message = TicketMessageRepository.get_message_by_id(message_id)

        if not message:
            raise ValueError("Message not found")

        ticket = TicketRepository.lock(
            message.ticket.id,
        )

        if ticket.status == TicketStatus.CLOSED:
            raise ValueError("Ticket closed")

        TicketRepository.update_status(
            ticket,
            status=TicketStatus.ANSWERED,
        )

        return
