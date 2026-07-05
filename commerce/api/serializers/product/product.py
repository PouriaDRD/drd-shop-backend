from rest_framework import serializers

from commerce.models import ProductModel
from .product_plan import ProductPlanSerializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = [
            "id",
            "slug",
            "title",
            "description",
            "type",
        ]
        read_only_fields = ["__all__"]


class ProductDetailSerializer(serializers.ModelSerializer):
    plans = ProductPlanSerializer(many=True, read_only=True)

    class Meta:
        model = ProductModel
        fields = [
            "id",
            "slug",
            "title",
            "description",
            "type",
            "plans",
        ]
        read_only_fields = ["__all__"]
