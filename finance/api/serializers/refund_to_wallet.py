from rest_framework import serializers
from finance.models import RefundToWalletRequestModel


class RefundToWalletRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying refund to wallet requests.
    """

    class Meta:
        model = RefundToWalletRequestModel
        fields = (
            "id",
            "amount",
            "reason",
            "status",
            "created_at",
        )
        read_only_fields = ["__all__"]
