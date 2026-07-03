import uuid
from django.db import models

from shop.enums import ProductType


class ProductModel(models.Model):
    """
    Product model.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
    )

    title = models.CharField(max_length=255)

    description = models.TextField(
        blank=True,
        null=True,
    )

    type = models.CharField(
        max_length=50,
        choices=ProductType.choices,
        default=ProductType.VPN,
    )

    is_active = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "products"
        ordering = ["-created_at"]

        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title
