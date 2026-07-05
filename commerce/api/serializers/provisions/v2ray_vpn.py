from rest_framework import serializers

from commerce.models import V2rayVPNModel


class V2rayVPNSerializer(serializers.ModelSerializer):
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
        model = V2rayVPNModel
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
