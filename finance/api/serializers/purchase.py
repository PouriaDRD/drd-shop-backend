from rest_framework import serializers
from finance.models import PurchaseRequestModel


class PurchaseRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying purchase requests.
    """

    class Meta:
        model = PurchaseRequestModel
        fields = (
            "id",
            "amount",
            "reason",
            "status",
            "is_processed",
            "created_at",
        )
        read_only_fields = ["__all__"]
