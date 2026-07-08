import uuid

from django.db import models

from .user import UserModel
from finance.models import TransactionModel

from billing.models import OrderModel
from accounts.enums import RewardStatus


class ReferralRewardModel(models.Model):
    """
    Reward generated from a completed order.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    inviter = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="referral_rewards",
    )

    invited_user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="generated_rewards",
    )

    order = models.OneToOneField(
        OrderModel,
        on_delete=models.CASCADE,
        related_name="referral_reward",
    )

    transaction = models.ForeignKey(
        TransactionModel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    order_amount = models.PositiveBigIntegerField()

    commission_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    reward_amount = models.PositiveBigIntegerField()

    status = models.CharField(
        max_length=20,
        choices=RewardStatus.choices,
        default=RewardStatus.PENDING,
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "referral_rewards"

        ordering = [
            "-created_at",
        ]

        verbose_name = "Referral Reward"

        verbose_name_plural = "Referral Rewards"

    def __str__(self):
        return f"{self.inviter} -> {self.reward_amount}"
