import uuid

from django.db import models

from accounts.models import UserModel

from .ticket import TicketModel


class TicketMessageModel(models.Model):
    """
    Ticket message model.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    ticket = models.ForeignKey(
        TicketModel,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    sender = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    message = models.TextField()

    is_staff_reply = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        db_table = "ticket_messages"

        ordering = ["created_at"]

        verbose_name = "Ticket Message"

        verbose_name_plural = "Ticket Messages"

    def __str__(self):

        return f"{str(self.ticket)} | {str(self.sender)}"
