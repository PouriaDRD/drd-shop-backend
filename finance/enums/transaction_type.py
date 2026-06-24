from django.db import models


class TransactionType(models.TextChoices):
    """
    Financial transaction types.
    """

    DEPOSIT = "deposit", "Deposit"

    PURCHASE = "purchase", "Purchase"

    REFUND = "refund", "Refund"
