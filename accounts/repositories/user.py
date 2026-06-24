from typing import Optional

from accounts.models import UserModel
from accounts.utils import (
    normalize_iranian_mobile,
    UserRole,
    UserStatus,
)


class UserRepository:
    """
    Repository layer for User database operations.
    Only handles ORM queries (no business logic).
    """

    @staticmethod
    def create_user(
        phone_number: str, email: Optional[str] = None, **extra_fields
    ) -> UserModel:
        """
        Create a new user.
        """

        phone_number = normalize_iranian_mobile(phone_number)

        if email:
            email = email.lower().strip()

        return UserModel.objects.create_user(  # type: ignore
            phone_number=phone_number,
            email=email,
            role=UserRole.USER,
            status=UserStatus.ACTIVE,
            **extra_fields,
        )

    @staticmethod
    def get_user_by_email(email: str) -> Optional[UserModel]:
        """
        Get active user by email.
        """

        return UserModel.objects.filter(
            email=email.lower().strip(),
            status=UserStatus.ACTIVE,
        ).first()

    @staticmethod
    def get_user_by_phone_number(phone_number: str) -> Optional[UserModel]:
        """
        Get active user by phone number.
        """

        phone_number = normalize_iranian_mobile(phone_number)

        return UserModel.objects.filter(
            phone_number=phone_number,
            status=UserStatus.ACTIVE,
        ).first()

    @staticmethod
    def update_user_password(user: UserModel, new_password: str) -> UserModel:
        """
        Update hashed password.
        """

        user.set_password(new_password)
        user.save()

        return user
