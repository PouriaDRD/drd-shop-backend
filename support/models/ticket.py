import uuid

from django.db import models

from accounts.models import UserModel

from support.enums.ticket import (
    TicketStatus,
    TicketPriority,
    TicketCategory,
)


class TicketModel(models.Model):
    """
    Ticket model.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="tickets",
    )

    title = models.CharField(
        max_length=255,
    )

    category = models.CharField(
        max_length=30,
        choices=TicketCategory.choices,
        default=TicketCategory.GENERAL,
    )

    priority = models.CharField(
        max_length=20,
        choices=TicketPriority.choices,
        default=TicketPriority.MEDIUM,
    )

    status = models.CharField(
        max_length=20,
        choices=TicketStatus.choices,
        default=TicketStatus.OPEN,
    )

    last_message_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        db_table = "tickets"

        ordering = ["-created_at"]

        verbose_name = "Ticket"

        verbose_name_plural = "Tickets"

    def __str__(self):

        return f"{str(self.title)} | {self.user}"
