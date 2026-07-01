from django.db import models


class RefundToWalletStatus(models.TextChoices):
    """
    Refund request lifecycle.
    """

    PENDING = "pending", "Pending"

    APPROVED = "approved", "Approved"

    REJECTED = "rejected", "Rejected"

    CANCELLED = "cancelled", "Cancelled"


class RefundToUserStatus(models.TextChoices):
    """
    Refund request lifecycle.
    """

    PENDING = "pending", "Pending"

    APPROVED = "approved", "Approved"

    REJECTED = "rejected", "Rejected"

    CANCELLED = "cancelled", "Cancelled"
