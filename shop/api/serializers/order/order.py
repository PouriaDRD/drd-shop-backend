from rest_framework import serializers

from shop.models import OrderModel

from .order_item import OrderItemSerializer


class OrderSerializer(serializers.ModelSerializer):
    """
    Order serializer.
    """

    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = OrderModel
        fields = (
            "id",
            "status",
            "total_price",
            "items",
            "created_at",
        )
        read_only_fields = ["__all__"]
