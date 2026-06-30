from rest_framework import serializers

from finance.models import WalletModel
from finance.repositories import WalletRepository


class WalletSerializer(serializers.ModelSerializer):
    """
    Wallet read serializer.
    """

    balance = serializers.SerializerMethodField()

    class Meta:
        model = WalletModel
        fields = ("balance",)

        read_only_fields = (
            "id",
            "balance",
            "created_at",
        )

    def get_balance(self, obj: WalletModel) -> int:
        """
        Return current wallet balance.
        """

        return WalletRepository.get_balance(obj)
