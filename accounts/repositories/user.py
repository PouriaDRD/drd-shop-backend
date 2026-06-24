from typing import Optional
from django.db import transaction
from django.utils import timezone

from accounts.models import UserModel
from accounts.utils import normalize_iranian_mobile, UserRole, UserStatus


class UserRepository:
    """
    Repository Layer:
    Only DB operations (CRUD).
    No business logic allowed.
    """

    @staticmethod
    @transaction.atomic
    def create_user(
        phone_number: str, email: Optional[str] = None, **extra_fields
    ) -> UserModel:
        """
        Create a new user in DB.

        Responsibility:
        - normalize inputs
        - persist user
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
    def get_by_email(email: str) -> Optional[UserModel]:
        """Fetch user by email."""
        return UserModel.objects.filter(email=email.lower().strip()).first()

    @staticmethod
    def get_by_phone(phone_number: str) -> Optional[UserModel]:
        """Fetch user by phone number."""
        return UserModel.objects.filter(
            phone_number=normalize_iranian_mobile(phone_number)
        ).first()

    @staticmethod
    def update_password(user: UserModel, new_password: str) -> UserModel:
        """Update hashed password."""
        user.set_password(new_password)
        user.save(update_fields=["password"])
        return user

    @staticmethod
    def update_last_login(user: UserModel) -> None:
        """
        Update last login timestamp.
        """
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])
