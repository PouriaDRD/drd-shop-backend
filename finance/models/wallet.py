import uuid

from django.db import models
from accounts.models import UserModel


class WalletModel(models.Model):
    """
    User wallet.
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

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "wallets"

        verbose_name = "Wallet"

        verbose_name_plural = "Wallets"

        ordering = ("-created_at",)

    def __str__(self):
        return str(self.user)
