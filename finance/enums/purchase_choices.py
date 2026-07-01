from django.db import models


class PurchaseStatus(models.TextChoices):
    """
    Purchase request lifecycle.
    """

    PENDING = "pending", "Pending"

    APPROVED = "approved", "Approved"

    REJECTED = "rejected", "Rejected"

    CANCELLED = "cancelled", "Cancelled"
