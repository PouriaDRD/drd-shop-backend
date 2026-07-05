from rest_framework import serializers

from commerce.models import ProductPlanModel
from .plan_feature import PlanFeatureSerializer


class ProductPlanSerializer(serializers.ModelSerializer):
    features = PlanFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = ProductPlanModel

        fields = [
            "id",
            "title",
            "description",
            "price",
            "is_available",
            "features",
        ]

        read_only_fields = ["__all__"]
