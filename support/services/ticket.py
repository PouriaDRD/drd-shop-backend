from django.db import transaction
from django.core.exceptions import PermissionDenied

from accounts.repositories import UserRepository

from support.repositories import (
    TicketRepository,
    TicketMessageRepository,
    TicketAttachmentRepository,
)

from support.models import TicketModel
from support.enums import (
    TicketStatus,
    TicketPriority,
    TicketCategory,
)

from notifications.tasks import send_email_task
from notifications.services import NotificationService


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

        TicketService.alert_admin(ticket)

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

        TicketService.alert_admin(ticket)

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

        NotificationService.create_success(
            user=user,
            title="تیکت بسته شد!",
            message=(f"تیکت با موضوع «{ticket.title}» بسته شد."),
        )

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

        NotificationService.create_success(
            user=ticket.user,
            title="پاسخ به تیکت ارسال شد!",
            message=(f"ما به تیکت شما با موضوغ «{ticket.title}» پاسخ دادیم."),
        )

        if ticket.user.email_verified:
            TicketService.send_reply_email(ticket.user, ticket)

        return

    @staticmethod
    def send_reply_email(user, ticket: TicketModel):

        category_map = {
            TicketCategory.GENERAL.value: "عمومی",
            TicketCategory.ORDER.value: "سفارش",
            TicketCategory.TECHNICAL.value: "فنی",
            TicketCategory.PAYMENT.value: "پرداخت",
        }

        send_email_task.delay(
            template_slug="reply-ticket",
            recipient_email=user.email,
            recipient_name=str(user),
            context={
                "name": str(user),
                "ticket_title": ticket.title,
                "ticket_category": category_map[ticket.category],
                "ticket_status": ticket.status,
                "site_name": "DRD Shop",
            },
        )  # type: ignore

    @staticmethod
    def alert_admin(ticket: TicketModel):
        """
        Send admin notification for ticket approval.
        """

        admin_user = UserRepository.get_admin_user()

        if not admin_user:
            return

        NotificationService.create_success(
            user=admin_user,
            title="تیکت جدید ثبت شد!",
            message=(
                f"یک تیکت جدید ثبت شد.\n"
                f"موضوع: {ticket.title}\n"
                f"کاربر: {ticket.user}\n"
            ),
        )


#         {{ name }}
# {{ site_name }}

# {{ ticket_id }}
# {{ ticket_title }}
# {{ ticket_category }}
# {{ ticket_priority }}
# {{ ticket_status }}

# {{ replied_by }}
# {{ replied_at }}

# {{ reply }}

# {{ ticket_url }}
