from django.db import models


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
