import uuid
from django.db import models

from .wallet import WalletModel
from .transaction import TransactionModel
from finance.enums import TransactionStatus


class RefundToWalletRequestModel(models.Model):
    """
    Refund request back to the user's wallet.

    Flow:
        PENDING
            ↓
        APPROVED
            ↓
        Transaction(type=REFUND_TO_WALLET)
            ↓
        LedgerEntry(+amount)
            ↓
        Wallet.balance += amount

        REJECTED / CANCELLED
            ↓
        Nothing changes
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    wallet = models.ForeignKey(
        WalletModel,
        on_delete=models.PROTECT,
        related_name="wallet_refund_requests",
    )

    transaction = models.OneToOneField(
        TransactionModel,
        on_delete=models.PROTECT,
        related_name="wallet_refund_request",
        null=True,
        blank=True,
    )

    amount = models.PositiveBigIntegerField()

    reason = models.TextField(
        help_text="Reason for issuing the refund.",
    )

    admin_note = models.TextField(
        blank=True,
        help_text="Internal note.",
    )

    status = models.CharField(
        max_length=20,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
    )

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
        db_table = "wallet_refund_requests"

        ordering = ["-created_at"]

        verbose_name = "Wallet Refund Request"

        verbose_name_plural = "Wallet Refund Requests"

    def __str__(self):
        return f"Wallet Refund #{self.id}"
