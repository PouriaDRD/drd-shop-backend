import uuid
from django.db import models
from django.db.models import Sum
from accounts.models import UserModel


class WalletModel(models.Model):
    """
    Wallet attached to a single user.

    Notes:
        - balance is a cached value for fast reads.
        - LedgerEntryModel is the source of truth.
        - Never update balance directly outside finance services.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.OneToOneField(
        UserModel,
        on_delete=models.PROTECT,
        related_name="wallet",
    )

    updated_at = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def balance(self):
        result = self.ledger_entries.aggregate(balance=Sum("amount"))  # type: ignore
        return int(result["balance"]) if result and not result["balance"] is None else 0

    class Meta:
        db_table = "wallets"

        ordering = ("-created_at",)

        verbose_name = "Wallet"

        verbose_name_plural = "Wallets"

    def __str__(self):
        return f"{self.user}'s wallet"
