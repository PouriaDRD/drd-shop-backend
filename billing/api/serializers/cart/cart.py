from rest_framework import serializers

from billing.models import CartModel
from .cart_item import CartItemSerializer


class CartSerializer(serializers.ModelSerializer):
    """
    Cart serializer.
    """

    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = CartModel
        fields = (
            "id",
            "subtotal",
            "discount",
            "total_price",
            "items",
        )
        read_only_fields = ["__all__"]
