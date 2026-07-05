import uuid
from django.db import models

from ..product import ProductModel
from commerce.enums import DiscountType


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
        help_text="Unique coupon code entered by the user (e.g. SAVE20).",
    )

    title = models.CharField(
        max_length=255,
        help_text="Internal title for admin display (not shown to customers).",
    )

    description = models.TextField(
        blank=True,
        help_text="Optional description explaining coupon rules or campaign details.",
    )

    discount_type = models.CharField(
        max_length=20,
        choices=DiscountType.choices,
        default=DiscountType.PERCENT,
        help_text="Type of discount: percentage-based or fixed amount.",
    )

    discount_value = models.PositiveIntegerField(
        help_text="Discount value. If percentage, this is 0–100. If fixed, it's the amount in smallest currency unit.",
    )

    max_discount = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Maximum discount cap (only applies for percentage-based discounts).",
    )

    minimum_order_amount = models.PositiveBigIntegerField(
        default=1,
        help_text="Minimum order subtotal required to apply this coupon.",
    )

    usage_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Maximum number of times this coupon can be used globally. Null = unlimited.",
    )

    used_count = models.PositiveIntegerField(
        default=0,
        help_text="Total number of times this coupon has been used (should be synced with usage records).",
    )

    per_user_limit = models.PositiveIntegerField(
        default=1,
        help_text="Maximum number of times a single user can use this coupon.",
    )

    starts_at = models.DateTimeField(
        help_text="Datetime when the coupon becomes active.",
    )

    expires_at = models.DateTimeField(
        help_text="Datetime when the coupon expires and becomes invalid.",
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Whether this coupon is active and can be used.",
    )

    allowed_products = models.ManyToManyField(
        ProductModel,
        blank=True,
        help_text="Restrict coupon to specific products. If empty, applies to all products.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the coupon was created.",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the coupon was last updated.",
    )

    class Meta:
        db_table = "coupons"
        ordering = ["-created_at"]
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"

    def __str__(self):
        return f"{self.title} ({self.code})"
