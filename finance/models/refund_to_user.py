import uuid
from django.db import models
from django.core.validators import (
    RegexValidator,
    FileExtensionValidator,
)

from .wallet import WalletModel
from .transaction import TransactionModel
from finance.enums import (
    RefundToUserStatus,
    DepositPaymentMethod,
)


def receipt_upload_path(instance, filename):
    ext = filename.rsplit(".", 1)[-1]
    return (
        f"receipts/refunds/"
        f"{instance.transaction.wallet.user.id}/"
        f"{instance.id}.{ext}"
    )


class RefundToUserRequestModel(models.Model):
    """
    Refund request directly to the user's bank account.

    Flow:
        PENDING
            ↓
        APPROVED
            ↓
        Transaction(type=REFUND_TO_USER)
            ↓
        LedgerEntry(-amount)
            ↓
        Wallet.balance -= amount

        Admin transfers money to user's account.

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
        related_name="user_refund_requests",
    )

    transaction = models.OneToOneField(
        TransactionModel,
        on_delete=models.PROTECT,
        related_name="user_refund_request",
        null=True,
        blank=True,
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

    receiver_name = models.CharField(
        max_length=255,
    )

    receiver_card_number = models.CharField(
        max_length=16,
        validators=[
            RegexValidator(
                regex=r"^\d{16}$",
                message="Invalid card number.",
            )
        ],
    )

    receiver_iban = models.CharField(
        max_length=26,
        blank=True,
        help_text="Optional IBAN (Sheba).",
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

    reason = models.TextField(
        blank=True,
        null=True,
        help_text="Reason for issuing the refund.",
    )

    admin_note = models.TextField(
        blank=True,
        null=True,
        help_text="Internal note.",
    )

    status = models.CharField(
        max_length=20,
        choices=RefundToUserStatus.choices,
        default=RefundToUserStatus.PENDING,
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
        db_table = "user_refund_requests"

        ordering = ["-created_at"]

        verbose_name = "User Refund Request"

        verbose_name_plural = "User Refund Requests"

    def save(self, *args, **kwargs):
        self.receiver_card_number = (
            self.receiver_card_number.replace("-", "").replace(" ", "").strip()
        )

        self.receiver_iban = (
            self.receiver_iban.replace(" ", "").replace("-", "").upper()
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"User Refund #{self.id}"
