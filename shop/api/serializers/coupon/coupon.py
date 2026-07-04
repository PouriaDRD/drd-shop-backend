from rest_framework import serializers

from shop.models import CouponModel


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponModel
        fields = (
            "id",
            "code",
            "discount_type",
            "value",
            "min_purchase",
            "max_discount",
        )
        read_only_fields = ["__all__"]
