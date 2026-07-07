from django.db import transaction

from support.models import TicketAttachmentModel


class TicketAttachmentRepository:
    """
    Database operations for ticket attachments.
    """

    @staticmethod
    @transaction.atomic
    def create(**kwargs) -> TicketAttachmentModel:
        """
        Create attachment.
        """

        return TicketAttachmentModel.objects.create(**kwargs)

    @staticmethod
    def get_ticket_attachments(
        ticket_id,
    ):
        return TicketAttachmentModel.objects.filter(
            ticket_id=ticket_id,
        ).order_by("-created_at")
