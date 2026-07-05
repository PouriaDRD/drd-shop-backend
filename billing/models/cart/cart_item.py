import uuid

from django.db import models

from .cart import CartModel
from commerce.models import ProductModel, ProductPlanModel


class CartItemModel(models.Model):
    """
    Shopping cart item.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    cart = models.ForeignKey(
        CartModel,
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

    unit_price = models.PositiveBigIntegerField()

    total_price = models.PositiveBigIntegerField()

    updated_at = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cart_items"

        verbose_name = "Cart Item"

        verbose_name_plural = "Cart Items"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "cart",
                    "product",
                    "plan",
                ],
                name="unique_cart_product_plan",
            )
        ]

    def __str__(self):
        return f"{self.product.title} ({self.plan.title})"
