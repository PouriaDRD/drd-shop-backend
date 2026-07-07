import uuid

from django.db import models

from .ticket_message import TicketMessageModel


def ticket_attachment_path(
    instance,
    filename,
):

    return f"tickets/" f"{instance.message.ticket.id}/" f"{filename}"


class TicketAttachmentModel(models.Model):
    """
    Ticket attachment model.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    message = models.ForeignKey(
        TicketMessageModel,
        on_delete=models.CASCADE,
        related_name="attachments",
    )

    file = models.FileField(
        upload_to=ticket_attachment_path,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        db_table = "ticket_attachments"

        ordering = ["created_at"]

        verbose_name = "Ticket Attachment"

        verbose_name_plural = "Ticket Attachments"

    def __str__(self):

        return f"{str(self.message)} | {str(self.file)}"
