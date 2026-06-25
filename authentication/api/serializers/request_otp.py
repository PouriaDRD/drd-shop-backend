from rest_framework import serializers
from accounts.utils import normalize_iranian_mobile, validate_iranian_mobile


class RequestOTPSerializer(serializers.Serializer):
    """
    Serializer for OTP requests.
    """

    phone_number = serializers.CharField(
        max_length=11,
        required=True,
        allow_blank=False,
        error_messages={
            "required": "Phone number is required.",
            "blank": "Phone number cannot be blank.",
        },
    )

    def validate_phone_number(self, value: str) -> str:
        """
        Normalize and validate phone number format.
        """

        normalized = normalize_iranian_mobile(value)

        validate_iranian_mobile(normalized)

        return normalized
