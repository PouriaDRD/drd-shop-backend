import uuid
from django.db import models

from .feature import FeatureModel
from .product_plan import ProductPlanModel


class PlanFeatureModel(models.Model):
    """
    Product plan feature. A product plan can have multiple features.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    plan = models.ForeignKey(
        ProductPlanModel,
        on_delete=models.CASCADE,
        related_name="features",
    )

    feature = models.ForeignKey(
        FeatureModel,
        on_delete=models.CASCADE,
    )

    value = models.CharField(max_length=255)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "plan_features"
        ordering = ["-created_at"]

        verbose_name = "Plan Feature"
        verbose_name_plural = "Plan Features"

    def __str__(self):
        return f"{self.plan.title} - {self.feature.title}"
