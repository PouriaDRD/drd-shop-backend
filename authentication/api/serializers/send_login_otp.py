from rest_framework import serializers

from authentication.services.auth import AuthService
from authentication.exceptions import UserNotFoundError, UserNotFoundError


class SendLoginOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs["email"]

        try:
            result = AuthService.send_login_otp(email)
        except UserNotFoundError:
            raise serializers.ValidationError({"email": "کاربری با این ایمیل یافت نشد"})

        attrs["result"] = result
        return attrs

    def create(self, validated_data):
        return validated_data["result"]
