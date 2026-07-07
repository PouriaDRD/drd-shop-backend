from rest_framework import serializers


class PurchaseStatisticsSerializer(serializers.Serializer):
    total_purchase_amount = serializers.BigIntegerField()

    last_30_days_purchase_amount = serializers.BigIntegerField()

    class Meta:
        fields = (
            "total_purchase_amount",
            "last_30_days_purchase_amount",
        )
        read_only_fields = (
            "total_purchase_amount",
            "last_30_days_purchase_amount",
        )
