import uuid
from django.db import models

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

    balance = models.BigIntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "wallets"

        ordering = ("-created_at",)

        verbose_name = "Wallet"

        verbose_name_plural = "Wallets"

    def __str__(self):
        return f"{self.user}'s wallet"
