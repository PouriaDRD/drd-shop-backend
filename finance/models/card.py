import uuid
from django.db import models
from django.core.validators import (
    RegexValidator,
)


class CardModel(models.Model):
    """
    Card model.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    owner_name = models.CharField(
        max_length=255,
    )

    owner_card_number = models.CharField(
        max_length=16,
        validators=[
            RegexValidator(
                regex=r"^\d{16}$",
                message="Invalid card number.",
            )
        ],
    )

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cards"

        ordering = ["-created_at"]

        verbose_name = "Card"

        verbose_name_plural = "Cards"

    def __str__(self):
        return f"{self.owner_name} - {self.owner_card_number}"
