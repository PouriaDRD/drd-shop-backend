import uuid
from django.db import models

from finance.enums import TransactionType
from .wallet import WalletModel
from .transaction import TransactionModel


class LedgerEntryModel(models.Model):
    """
    Immutable financial ledger.

    Source of truth for every balance change.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    transaction = models.OneToOneField(
        TransactionModel,
        on_delete=models.PROTECT,
        related_name="ledger_entry",
    )

    wallet = models.ForeignKey(
        WalletModel,
        on_delete=models.PROTECT,
        related_name="ledger_entries",
    )

    transaction_type = models.CharField(
        max_length=30,
        choices=TransactionType.choices,
    )

    amount = models.BigIntegerField()

    balance_before = models.BigIntegerField()

    balance_after = models.BigIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ledger_entries"

        ordering = ["-created_at"]

        verbose_name = "Ledger Entry"

        verbose_name_plural = "Ledger Entries"

    def __str__(self):
        return f"{self.transaction_type} | {self.amount:,}"
