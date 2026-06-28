from rest_framework import serializers

from authentication.services.auth import AuthService
from authentication.exceptions import (
    UserNotFoundError,
    InvalidOTPError,
    UserNotFoundError,
)


class VerifyLoginOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()
    code = serializers.CharField()

    def validate(self, attrs):

        email = attrs["email"]
        code = attrs["code"]

        try:
            result = AuthService.verify_login_otp(email, code)
        except InvalidOTPError:
            raise serializers.ValidationError(
                {"code": "کد وارد شده اشتباه یا منقضی شده است"}
            )
        except UserNotFoundError:
            raise serializers.ValidationError({"email": "کاربر یافت نشد"})

        attrs["result"] = result
        return attrs

    def create(self, validated_data):
        return validated_data["result"]
