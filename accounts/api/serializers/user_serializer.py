from rest_framework import serializers

from accounts.models import UserModel
from finance.api.serializers import WalletSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for UserModel.
    """

    referral_code = serializers.SerializerMethodField()
    total_referrals = serializers.SerializerMethodField()
    total_paid = serializers.SerializerMethodField()

    wallet = WalletSerializer(read_only=True)

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
            "referral_code",
            "total_referrals",
            "total_paid",
            "wallet",
        )

        read_only_fields = [
            "__all__",
        ]

    def get_referral_code(self, obj):
        """
        Return user's referral code.
        """

        if hasattr(obj, "referral_code"):
            return obj.referral_code.code

        return None

    def get_total_referrals(self, obj):
        """
        Return total referral signups.
        """

        if hasattr(obj, "referral_code"):
            return obj.referral_code.signups

        return 0

    def get_total_paid(self, obj):
        """
        Return total referral signups.
        """

        if hasattr(obj, "referral_code"):
            return obj.referral_code.total_paid
