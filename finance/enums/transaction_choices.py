from django.db import models


class TransactionStatus(models.TextChoices):
    """
    Financial transaction lifecycle.
    """

    PENDING = "pending", "Pending"

    APPROVED = "approved", "Approved"

    REJECTED = "rejected", "Rejected"

    CANCELLED = "cancelled", "Cancelled"


class TransactionType(models.TextChoices):
    """
    Supported financial transaction types.
    """

    DEPOSIT = "deposit", "Deposit"

    PURCHASE = "purchase", "Purchase"

    REFUND_TO_WALLET = "refund_to_wallet", "Refund To Wallet"

    REFUND_TO_USER = "refund_to_user", "Refund To User"

    WITHDRAW = "withdraw", "Withdraw"

    ADJUSTMENT = "adjustment", "Adjustment"
