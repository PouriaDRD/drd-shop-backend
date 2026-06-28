from typing import Optional
from django.db import transaction
from django.utils import timezone
from accounts.models import UserModel
from accounts.enums import UserRole, UserStatus


class UserRepository:
    """
    Repository Layer:
    Only DB operations (CRUD).
    No business logic allowed.
    """

    @staticmethod
    @transaction.atomic
    def create_user(email: str, password: Optional[str] = None, **kwargs) -> UserModel:
        """
        Create a new user in DB.

        Responsibility:
        - normalize inputs
        - persist user
        """

        email = email.lower().strip()

        new_user = UserModel.objects.create_user(  # type: ignore
            email=email,
            email_verified=False,
            role=UserRole.USER,
            status=UserStatus.ACTIVE,
            password=password,
            **kwargs,
        )

        return new_user

    @staticmethod
    def get_by_email(email: str) -> Optional[UserModel]:
        """Fetch user by email."""
        result = UserModel.objects.filter(email=email.lower().strip()).first()
        return result

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
