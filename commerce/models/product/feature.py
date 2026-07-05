import uuid
from django.db import models


class FeatureModel(models.Model):
    """
    Product feature. A product can have multiple features.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    key = models.CharField(max_length=100, unique=True)
    # location, bandwidth, traffic, protocol, device_limit, days, etc.

    title = models.CharField(max_length=255)

    value_type = models.CharField(
        max_length=30,
        choices=[
            ("string", "String"),
            ("int", "Integer"),
            ("float", "Float"),
            ("bool", "Boolean"),
        ],
    )

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "features"
        ordering = ["-created_at"]

        verbose_name = "Feature"
        verbose_name_plural = "Features"

    def __str__(self):
        return self.title
