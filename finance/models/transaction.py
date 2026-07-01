import uuid
from django.db import models

from finance.enums import (
    TransactionStatus,
    TransactionType,
)
from .wallet import WalletModel


class TransactionModel(models.Model):
    """
    Financial transaction.

    Created only after a request has been processed.

    Every approved transaction must generate exactly one
    LedgerEntryModel.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    wallet = models.ForeignKey(
        WalletModel,
        on_delete=models.PROTECT,
        related_name="transactions",
    )

    amount = models.PositiveBigIntegerField()

    type = models.CharField(
        max_length=30,
        choices=TransactionType.choices,
    )

    status = models.CharField(
        max_length=20,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
    )

    description = models.TextField(blank=True)

    is_processed = models.BooleanField(
        default=False,
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transactions"

        ordering = ["-created_at"]

        verbose_name = "Transaction"

        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.type} | {self.amount:,}"
