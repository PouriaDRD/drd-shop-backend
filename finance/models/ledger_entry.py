import uuid

from django.db import models
from django.conf import settings

from .wallet import WalletModel
from .transaction import TransactionModel


class LedgerEntryModel(models.Model):
    """
    Immutable wallet entry.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    wallet = models.ForeignKey(
        WalletModel,
        on_delete=models.PROTECT,
        related_name="ledger_entries",
    )

    transaction = models.ForeignKey(
        TransactionModel,
        on_delete=models.PROTECT,
        related_name="entries",
    )

    amount = models.BigIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "ledger_entries"

        verbose_name = "Ledger Entry"

        verbose_name_plural = "Ledger Entries"

        ordering = [
            "-created_at",
        ]

        indexes = [
            models.Index(
                fields=[
                    "wallet",
                    "created_at",
                ]
            ),
        ]

    def __str__(self):
        return f"{self.id}"
