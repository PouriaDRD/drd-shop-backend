from rest_framework import serializers

from authentication.enums import OTPType
from authentication.services.auth import AuthService
from authentication.exceptions import UserNotFoundError, UserNotFoundError


class SendLoginOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_type = serializers.ChoiceField(choices=OTPType.choices, default=OTPType.LOGIN)

    def validate(self, attrs):
        email = attrs["email"]
        otp_type = attrs["otp_type"]
        try:
            result = AuthService.send_login_otp(email, otp_type)
        except UserNotFoundError:
            raise serializers.ValidationError({"email": "کاربری با این ایمیل یافت نشد"})

        attrs["result"] = result
        return attrs

    def create(self, validated_data):
        return validated_data["result"]
