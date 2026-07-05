from rest_framework import serializers


class ApplyCouponSerializer(serializers.Serializer):
    code = serializers.CharField()
