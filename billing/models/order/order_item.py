import uuid
from django.db import models

from .order import OrderModel
from commerce.models import ProductModel, ProductPlanModel


class OrderItemModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    order = models.ForeignKey(
        OrderModel,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        ProductModel,
        on_delete=models.PROTECT,
    )

    plan = models.ForeignKey(
        ProductPlanModel,
        on_delete=models.PROTECT,
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.PositiveBigIntegerField()

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "order_items"
        ordering = ["-created_at"]

        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f"{self.product.title} - {self.plan.title} x {self.quantity} for {self.order.user.email}"
