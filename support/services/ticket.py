from django.db import transaction
from django.core.exceptions import PermissionDenied

from support.repositories import TicketRepository, TicketMessageRepository


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
        subject: str,
        message: str,
        priority: str = TicketPriority.MEDIUM,
    ):

        ticket = TicketRepository.create(
            user=user,
            subject=subject,
            priority=priority,
            status=TicketStatus.OPEN,
        )

        TicketMessageRepository.create(
            ticket=ticket,
            sender=user,
            message=message,
            is_staff=False,
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
    ):

        ticket = TicketRepository.lock(
            ticket_id,
        )

        if ticket.user.id != user.id:
            raise PermissionDenied("Invalid ticket owner.")

        if ticket.status == TicketStatus.CLOSED:
            raise ValueError("Ticket is closed.")

        return TicketMessageRepository.create(
            ticket=ticket,
            sender=user,
            message=message,
            is_staff=False,
        )

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
