from rest_framework import serializers
from django.core.validators import EmailValidator

from authentication.services import AuthService


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

        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "رمز عبور مطابقت ندارد."}
            )

        attrs.pop("password_confirm")

        return attrs

    def create(self, validated_data):

        result = AuthService.register(**validated_data)

        return result
