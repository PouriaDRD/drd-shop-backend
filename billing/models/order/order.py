import uuid
from django.db import models

from billing.enums import OrderStatus
from accounts.models import UserModel
from commerce.models import CouponModel


class OrderModel(models.Model):
    """
    Order model. A user can have multiple orders.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    status = models.CharField(
        max_length=30,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )

    coupon = models.ForeignKey(
        CouponModel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    discount_amount = models.PositiveBigIntegerField(default=0)

    subtotal = models.PositiveBigIntegerField(default=0)

    total_price = models.PositiveBigIntegerField()

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "orders"
        ordering = ["-created_at"]

        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order #{str(self.id)[:8]} - {self.user.email}"
