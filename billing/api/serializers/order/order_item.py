from rest_framework import serializers

from billing.models import OrderItemModel
from commerce.api.serializers import ProductPlanSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Order item serializer.
    """

    product_id = serializers.UUIDField(
        source="product.id",
        read_only=True,
    )

    product_title = serializers.CharField(
        source="product.title",
        read_only=True,
    )

    plan = ProductPlanSerializer(
        read_only=True,
    )

    class Meta:
        model = OrderItemModel
        fields = (
            "id",
            "product_id",
            "product_title",
            "plan",
            "quantity",
            "price",
        )

        read_only_fields = ["__all__"]
