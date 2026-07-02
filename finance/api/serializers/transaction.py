from rest_framework import serializers
from finance.models import TransactionModel


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransactionModel
        fields = [
            "id",
            "amount",
            "type",
            "status",
            "payment_method",
            "description",
            "created_at",
        ]
        read_only_fields = ["__all__"]
