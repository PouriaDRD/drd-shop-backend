import uuid
from django.db import models

from .wallet import WalletModel
from finance.enums import PurchaseStatus
from .transaction import TransactionModel


class PurchaseRequestModel(models.Model):
    """
    Purchase request.

    APPROVED ->
        Transaction ->
        Ledger ->
        Wallet.balance update
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    wallet = models.ForeignKey(
        WalletModel,
        on_delete=models.PROTECT,
        related_name="purchase_requests",
    )

    transaction = models.OneToOneField(
        TransactionModel,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="purchase_request",
    )

    amount = models.PositiveBigIntegerField()

    status = models.CharField(
        max_length=20,
        choices=PurchaseStatus.choices,
        default=PurchaseStatus.PENDING,
    )

    admin_note = models.TextField(
        blank=True,
    )

    is_processed = models.BooleanField(
        default=False,
    )

    reviewed_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    updated_at = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "purchase_requests"

        ordering = ["-created_at"]

        verbose_name = "Purchase Request"

        verbose_name_plural = "Purchase Requests"

    def __str__(self):
        return f"Purchase #{self.id}"
