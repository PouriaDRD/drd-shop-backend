import uuid
from django.db import models


class V2rayVPNModel(models.Model):
    """
    VPN provisioned service. A user can have multiple provisioned services.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    order_item = models.ForeignKey(
        "billing.OrderItemModel",
        on_delete=models.CASCADE,
    )

    subscription_link = models.URLField()
    content = models.TextField()

    expires_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "vpn_provisioned_services"
        ordering = ["-created_at"]

        verbose_name = "VPN Provisioned Service"
        verbose_name_plural = "VPN Provisioned Services"

    def __str__(self):
        return f"{self.order_item.product.title} - {self.order_item.plan.title}"
