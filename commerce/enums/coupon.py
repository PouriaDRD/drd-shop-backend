from django.db import models


class DiscountType(models.TextChoices):
    PERCENT = "percent", "Percent"
    FIXED = "fixed", "Fixed Amount"
