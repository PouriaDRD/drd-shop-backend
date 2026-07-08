import uuid
from django.db import models
from .user import UserModel


class ReferralCodeModel(models.Model):
    """
    Each user owns exactly one referral code.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name="referral_code",
    )

    code = models.CharField(
        unique=True,
        max_length=30,
    )

    clicks = models.PositiveIntegerField(
        default=0,
    )

    signups = models.PositiveIntegerField(
        default=0,
    )

    orders = models.PositiveIntegerField(
        default=0,
    )

    total_earned = models.PositiveBigIntegerField(
        default=0,
    )

    total_paid = models.PositiveBigIntegerField(
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "referral_codes"

        ordering = [
            "-created_at",
        ]

        verbose_name = "Referral Code"

        verbose_name_plural = "Referral Codes"

    def __str__(self):
        return f"{self.code} - {self.user}"
