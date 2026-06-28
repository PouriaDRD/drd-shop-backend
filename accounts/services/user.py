from typing import Optional
from rest_framework.exceptions import ValidationError

from finance.services import WalletService
from accounts.repositories import UserRepository


class UserService:
    """
    Business logic for user management.
    """

    @staticmethod
    def create_user(email: str, password: Optional[str] = None, **extra_fields):
        """
        Business rules:
        - user must be unique
        """

        if email and UserRepository.get_by_email(email):
            raise ValidationError({"email": "کاربری با این ایمیل قبلا ثبت شده است."})

        new_user = UserRepository.create_user(email, password, **extra_fields)
        wallet = WalletService.create_wallet(new_user)

        return new_user
