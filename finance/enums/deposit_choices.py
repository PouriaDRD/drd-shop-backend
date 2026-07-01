from django.db import models


class DepositStatus(models.TextChoices):
    """
    Deposit request lifecycle.
    """

    PENDING = "pending", "Pending"

    APPROVED = "approved", "Approved"

    REJECTED = "rejected", "Rejected"

    CANCELLED = "cancelled", "Cancelled"


class DepositPaymentMethod(models.TextChoices):
    """
    Supported deposit payment methods.
    """

    CARD_TO_CARD = "card_to_card", "Card To Card"

    ONLINE_GATEWAY = "online_gateway", "Online Gateway"
