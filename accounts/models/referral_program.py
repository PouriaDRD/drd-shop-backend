import uuid
from decimal import Decimal
from django.db import models


class ReferralProgramModel(models.Model):
    """
    Global referral settings.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=100,
        default="Default",
    )

    commission_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("10.00"),
    )

    minimum_order_amount = models.PositiveBigIntegerField(
        default=0,
    )

    reward_delay_days = models.PositiveIntegerField(
        default=7,
    )

    maximum_reward_amount = models.PositiveBigIntegerField(
        null=True,
        blank=True,
    )

    is_enabled = models.BooleanField(
        default=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "referral_program"

        verbose_name = "Referral Program"

        verbose_name_plural = "Referral Programs"

    def __str__(self):
        return self.name
