from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from accounts.models import UserModel
from accounts.services import UserService
from accounts.utils import UserStatus, UserRole, normalize_iranian_mobile


class UserAuthSerializer(serializers.Serializer):
    """
    Serializer for user authentication.
    """

    phone_number = serializers.CharField(max_length=11)

    def validate_phone_number(self, value):
        """
        Validate phone number.
        """

        if not UserService.is_phone_number_valid(value):
            raise ValidationError("Invalid phone number.")

        return normalize_iranian_mobile(value)
