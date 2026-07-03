import uuid
from django.db import models
from django.core.validators import (
    RegexValidator,
    FileExtensionValidator,
)

from .wallet import WalletModel
from .transaction import TransactionModel
from finance.enums import (
    DepositStatus,
    DepositPaymentMethod,
)


def receipt_upload_path(instance, filename):
    ext = filename.rsplit(".", 1)[-1]
    return f"receipts/deposits/" f"{instance.wallet.user.id}/" f"{instance.id}.{ext}"


class DepositRequestModel(models.Model):
    """
    Deposit request submitted by the user.

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
        related_name="deposit_requests",
    )

    transaction = models.OneToOneField(
        TransactionModel,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="deposit_request",
    )

    amount = models.PositiveBigIntegerField()

    payment_method = models.CharField(
        max_length=30,
        choices=DepositPaymentMethod.choices,
        default=DepositPaymentMethod.CARD_TO_CARD,
    )

    reference_number = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    tracking_code = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    sender_name = models.CharField(
        max_length=255,
    )

    sender_card_number = models.CharField(
        max_length=16,
        validators=[
            RegexValidator(
                regex=r"^\d{16}$",
                message="Invalid card number.",
            )
        ],
    )

    transaction_date = models.DateField(
        blank=True,
        null=True,
    )

    transaction_time = models.TimeField(
        blank=True,
        null=True,
    )

    receipt_image = models.ImageField(
        upload_to=receipt_upload_path,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
    )

    note = models.TextField(
        blank=True,
        null=True,
        help_text="User note.",
    )

    status = models.CharField(
        max_length=20,
        choices=DepositStatus.choices,
        default=DepositStatus.PENDING,
    )

    admin_note = models.TextField(
        blank=True,
        null=True,
        help_text="Internal note.",
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
        db_table = "deposit_requests"

        ordering = ["-created_at"]

        verbose_name = "Deposit Request"

        verbose_name_plural = "Deposit Requests"

    def save(self, *args, **kwargs):
        if self.sender_card_number:
            self.sender_card_number = (
                self.sender_card_number.replace("-", "").replace(" ", "").strip()
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Deposit #{self.id}"
