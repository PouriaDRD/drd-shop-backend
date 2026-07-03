from rest_framework import serializers

from finance.models import WalletModel
from finance.repositories import WalletRepository


class WalletSerializer(serializers.ModelSerializer):
    """
    Wallet read serializer.
    """

    class Meta:
        model = WalletModel
        fields = ("balance",)
        read_only_fields = ["__all__"]
