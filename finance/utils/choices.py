from django.db import models


class TransactionType(models.TextChoices):
    """
    Financial transaction types.
    """

    DEPOSIT = "deposit", "Deposit"

    PURCHASE = "purchase", "Purchase"

    REFUND = "refund", "Refund"


class TransactionStatus(models.TextChoices):
    """
    Transaction lifecycle status.
    """

    PENDING = "pending", "Pending"

    COMPLETED = "completed", "Completed"

    REJECTED = "rejected", "Rejected"


class PaymentMethod(models.TextChoices):
    """
    Payment methods.
    """

    CARD_TO_CARD = (
        "card_to_card",
        "Card To Card",
    )

    ADMIN = (
        "admin",
        "Admin",
    )
