from accounts.models import UserModel
from rest_framework import serializers

# from finance.api.serializers import WalletSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for UserModel.
    """

    # wallet = WalletSerializer(read_only=True)

    class Meta:
        model = UserModel
        fields = (
            "id",
            "email",
            "email_verified",
            "role",
            "status",
            "last_login",
            "created_at",
            # "wallet",
        )
        read_only_fields = ["__all__"]
