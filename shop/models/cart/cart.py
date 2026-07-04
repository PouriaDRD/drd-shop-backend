import uuid

from django.db import models

from ..coupon import CouponModel
from accounts.models import UserModel


class CartModel(models.Model):
    """
    Shopping cart.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name="cart",
    )

    coupon = models.ForeignKey(
        CouponModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="carts",
    )

    subtotal = models.PositiveBigIntegerField(default=0)

    discount = models.PositiveBigIntegerField(default=0)

    total_price = models.PositiveBigIntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "carts"

        verbose_name = "Cart"

        verbose_name_plural = "Carts"

    def __str__(self):
        return f"{self.user.email}'s cart"
