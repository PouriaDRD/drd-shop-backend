import uuid

from django.conf import settings
from django.db import models

from .wallet import WalletModel
from finance.utils import (
    PaymentMethod,
    TransactionStatus,
    TransactionType,
)


class TransactionModel(models.Model):
    """
    Financial transaction.
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

    amount = models.BigIntegerField()

    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices,
        default=TransactionType.DEPOSIT,
    )

    status = models.CharField(
        max_length=20,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
    )

    payment_method = models.CharField(
        max_length=30,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CARD_TO_CARD,
    )

    description = models.TextField(
        blank=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "transactions"

        verbose_name = "Transaction"

        verbose_name_plural = "Transactions"

        ordering = [
            "-created_at",
        ]

    def __str__(self):
        return f"{self.id}"
