from rest_framework import serializers
from django.core.validators import EmailValidator

from authentication.services import AuthService
from accounts.repositories import ReferralCodeRepository


class RegisterSerializer(serializers.Serializer):
    """
    Serializer for registering a user.
    """

    email = serializers.EmailField(
        required=True,
        validators=[EmailValidator],
        error_messages={
            "required": "ایمیل اجباری است",
            "blank": "ایمیل نمی تواند خالی باشد",
        },
    )

    referral_code = serializers.CharField(
        required=True,
        error_messages={
            "blank": "این فیلد اجباری است",
            "invalid": "کد دعوت اشتباه است",
        },
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"},
        error_messages={
            "required": "رمز عبور اجباری است",
            "blank": "رمز عبور نمی تواند خالی باشد",
        },
    )

    password_confirm = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"},
        error_messages={
            "required": "تایید رمز عبور اجباری است",
            "blank": "تایی عبور نمی تواند خالی باشد",
        },
    )

    def validate(self, attrs):

        referral_code = attrs.get("referral_code")

        if not referral_code:
            raise serializers.ValidationError(
                {"referral_code": "کد دعوت اجباری است."},
                code="invalid_code",
            )

        res = ReferralCodeRepository.get_by_code(referral_code)

        if not res:
            raise serializers.ValidationError(
                {"referral_code": "کد دعوت نامعتبر است."},
                code="invalid_code",
            )

        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "رمز عبور مطابقت ندارد."}
            )

        attrs.pop("password_confirm")

        return attrs

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        referral_code = validated_data.get("referral_code")
        request = self.context.get("request")

        result = AuthService.register(
            email=email,
            password=password,
            referral_code=referral_code,
            request=request,  # type: ignore
        )

        return result
