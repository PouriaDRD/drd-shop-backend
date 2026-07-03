import uuid
from django.db import models

from shop.enums import DiscountType


class CouponModel(models.Model):
    """
    Global discount coupon.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    code = models.CharField(
        max_length=50,
        unique=True,
    )

    title = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    discount_type = models.CharField(
        max_length=20,
        choices=DiscountType.choices,
    )

    discount_value = models.PositiveIntegerField()

    max_discount = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    minimum_order_amount = models.PositiveBigIntegerField(
        default=1,
    )

    usage_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    used_count = models.PositiveIntegerField(
        default=0,
    )

    per_user_limit = models.PositiveIntegerField(
        default=1,
    )

    starts_at = models.DateTimeField()

    expires_at = models.DateTimeField()

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "coupons"

        ordering = ["-created_at"]

        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"

    def __str__(self):
        return f"{self.title} ({self.code})"
