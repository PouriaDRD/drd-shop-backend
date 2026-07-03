from rest_framework import serializers

from finance.models import RefundToUserRequestModel


class RefundToUserRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying deposit requests.
    """

    class Meta:
        model = RefundToUserRequestModel
        fields = (
            "id",
            "amount",
            "payment_method",
            "reference_number",
            "tracking_code",
            "receiver_name",
            "receiver_card_number",
            "receiver_iban",
            "transaction_date",
            "transaction_time",
            "reason",
            "status",
            "is_processed",
            "created_at",
        )
        read_only_fields = ["__all__"]
