import uuid
from django.db import models

from .coupon import CouponModel


class CouponUsageModel(models.Model):
    """
    Coupon usage history.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    coupon = models.ForeignKey(
        CouponModel,
        on_delete=models.PROTECT,
        related_name="usages",
    )

    wallet = models.ForeignKey(
        "finance.WalletModel",
        on_delete=models.PROTECT,
        related_name="coupon_usages",
    )

    order = models.ForeignKey(
        "billing.OrderModel",
        on_delete=models.PROTECT,
        related_name="coupon_usages",
    )

    discount_amount = models.PositiveBigIntegerField()

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "coupon_usages"

        ordering = ["-created_at"]

        verbose_name = "Coupon Usage"
        verbose_name_plural = "Coupon Usages"

        unique_together = (
            "coupon",
            "wallet",
            "order",
        )

    def __str__(self):
        return f"{self.coupon.code} | {self.wallet.user}"
