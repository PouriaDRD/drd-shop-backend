from rest_framework import serializers
from commerce.models import CouponModel


class ApplyCouponSerializer(serializers.Serializer):
    code = serializers.CharField(
        required=True,
        error_messages={
            "required": "Coupon code is required.",
            "blank": "Coupon code is required.",
        },
    )

    class Meta:
        fields = ("code",)

    def validate(self, attrs):
        code = attrs["code"]
        coupon = CouponModel.objects.filter(
            code=code,
            is_active=True,
        ).first()

        if not coupon:
            raise serializers.ValidationError("Invalid coupon code.")

        return attrs
