from rest_framework import serializers

from shop.models import OrderItemModel

from ..product import ProductPlanSerializer


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

    product_slug = serializers.CharField(
        source="product.slug",
        read_only=True,
    )

    product_type = serializers.CharField(
        source="product.type",
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
            "product_slug",
            "product_type",
            "plan",
            "quantity",
            "price",
        )
