from rest_framework import serializers


class AddCartItemSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    plan_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1, default=1)
    is_renewal = serializers.BooleanField(default=False, required=False)


class AddCartItemsSerializer(serializers.Serializer):
    items = AddCartItemSerializer(many=True)


class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
