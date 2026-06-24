from rest_framework import serializers

from accounts.services import UserService
from accounts.utils import normalize_iranian_mobile


class VerifyOTPSerializer(serializers.Serializer):
    """
    Serializer for OTP verification.
    """

    otp_id = serializers.UUIDField()

    code = serializers.CharField(
        max_length=6,
        error_messages={
            "required": "Code is required",
            "blank": "Code cannot be blank",
        },
    )

    phone_number = serializers.CharField(
        max_length=11,
        error_messages={
            "required": "Phone number is required",
            "blank": "Phone number cannot be blank",
        },
    )

    def validate_phone_number(self, value):
        """
        Basic format validation.
        (Business validation is in service layer)
        """
        if not value:
            raise serializers.ValidationError("Phone number is required.")

        normalized = normalize_iranian_mobile(value)
        if not UserService.is_phone_valid(normalized):
            raise serializers.ValidationError("Invalid phone number.")

        return normalized
