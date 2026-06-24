from typing import Optional

from django.db import transaction
from rest_framework.exceptions import ValidationError

from accounts.models import UserModel
from accounts.repositories import UserRepository


class UserService:
    """
    Service layer for user business logic.
    """

    @staticmethod
    @transaction.atomic
    def create_user(phone_number: str, email: Optional[str] = None, **extra_fields):
        """
        Create user with uniqueness validation.
        """

        if UserRepository.get_user_by_phone_number(phone_number):
            raise ValidationError({"phone_number": "User already exists."})

        if email and UserRepository.get_user_by_email(email):
            raise ValidationError({"email": "User already exists."})

        new_user = UserRepository.create_user(phone_number, email, **extra_fields)

        return new_user

    @staticmethod
    @transaction.atomic
    def update_user_password(user: UserModel, new_password: str):
        """
        Update user password.
        """

        return UserRepository.update_user_password(user, new_password)
