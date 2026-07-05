import uuid
from django.db import models

from .product import ProductModel


class ProductPlanModel(models.Model):
    """
    Product plan. A product can have multiple plans.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    product = models.ForeignKey(
        ProductModel,
        on_delete=models.CASCADE,
        related_name="plans",
    )

    title = models.CharField(max_length=255)  # "Germany 30 days 100GB"

    description = models.TextField(
        blank=True,
        null=True,
    )

    price = models.PositiveBigIntegerField()

    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "product_plans"
        ordering = ["-created_at"]

        verbose_name = "Product Plan"
        verbose_name_plural = "Product Plans"

    def __str__(self):
        return self.title
