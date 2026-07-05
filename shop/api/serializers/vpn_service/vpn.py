from rest_framework import serializers

from shop.models import VPNProvisionedServiceModel


class VPNSerializer(serializers.ModelSerializer):
    """
    VPN service serializer.
    """

    product_title = serializers.CharField(
        source="order_item.product.title",
        read_only=True,
    )
    plan_title = serializers.CharField(
        source="order_item.plan.title",
        read_only=True,
    )

    class Meta:
        model = VPNProvisionedServiceModel
        fields = (
            "id",
            "product_title",
            "plan_title",
            "subscription_link",
            "content",
            "expires_at",
            "created_at",
        )
        read_only_fields = fields
