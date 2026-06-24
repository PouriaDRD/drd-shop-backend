from django.db import models


class TransactionStatus(models.TextChoices):
    """
    Transaction lifecycle status.
    """

    PENDING = "pending", "Pending"

    COMPLETED = "completed", "Completed"

    REJECTED = "rejected", "Rejected"
