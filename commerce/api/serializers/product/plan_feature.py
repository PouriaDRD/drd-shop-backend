from rest_framework import serializers
from commerce.models import PlanFeatureModel


class PlanFeatureSerializer(serializers.ModelSerializer):
    feature = serializers.CharField(source="feature.title")

    class Meta:
        model = PlanFeatureModel
        fields = [
            "feature",
            "value",
        ]
        read_only_fields = ["__all__"]
