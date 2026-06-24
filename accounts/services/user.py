from typing import Optional
from rest_framework.exceptions import ValidationError

from finance.services import WalletService
from accounts.repositories import UserRepository
from accounts.utils import validate_iranian_mobile


class UserService:
    """
    Business logic for user management.
    """

    @staticmethod
    def create_user(phone_number: str, email: Optional[str] = None, **extra_fields):
        """
        Business rules:
        - user must be unique
        """

        if UserRepository.get_by_phone(phone_number):
            raise ValidationError({"phone_number": "User already exists."})

        if email and UserRepository.get_by_email(email):
            raise ValidationError({"email": "User already exists."})

        new_user = UserRepository.create_user(phone_number, email, **extra_fields)
        wallet = WalletService.create_wallet(new_user)

        return new_user

    @staticmethod
    def is_phone_valid(phone_number: str) -> bool:
        """Validate Iranian phone number format."""
        try:
            validate_iranian_mobile(phone_number)
            return True
        except ValidationError:
            return False
