from rest_framework import serializers

from billing.models import CartItemModel


class CartItemSerializer(serializers.ModelSerializer):
    """
    Cart item detail serializer.
    """

    product_id = serializers.UUIDField(source="product.id", read_only=True)
    plan_id = serializers.UUIDField(source="plan.id", read_only=True)
    plan_title = serializers.CharField(source="plan.title")

    class Meta:
        model = CartItemModel
        fields = (
            "id",
            "product_id",
            "plan_title",
            "plan_id",
            "quantity",
            "unit_price",
            "total_price",
        )
