from django.contrib.auth.base_user import BaseUserManager


from accounts.utils import (
    normalize_iranian_mobile,
    validate_iranian_mobile,
    UserRole,
    UserStatus,
)


class UserManager(BaseUserManager):
    """
    Custom user manager using phone_number as USERNAME_FIELD.
    Supports optional password (e.g. OTP-based auth).
    """

    def _create_user(self, phone_number, password=None, **extra_fields):
        """
        Internal method to create a user with optional password.
        """

        # Validate required field
        if not phone_number:
            raise ValueError("Phone number is required")

        # Normalize phone number
        phone_number = normalize_iranian_mobile(phone_number)

        if phone_number is None:
            raise ValueError("Invalid phone number")

        # Validate format
        validate_iranian_mobile(phone_number)

        # Create user instance
        user = self.model(
            phone_number=phone_number,
            **extra_fields,
        )

        # OPTIONAL PASSWORD HANDLING
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        # Validate model
        user.full_clean()

        # Save user
        user.save(using=self._db)

        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Create a normal user (password optional).
        """

        extra_fields.setdefault("status", UserStatus.ACTIVE)
        extra_fields.setdefault("role", UserRole.USER)

        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Create a superuser (password required).
        """

        extra_fields.setdefault("status", UserStatus.ACTIVE)
        extra_fields.setdefault("role", UserRole.SUPERUSER)

        if not password:
            raise ValueError("Superuser must have a password")

        if extra_fields.get("role") != UserRole.SUPERUSER:
            raise ValueError("Superuser must have role=SUPERUSER")

        if extra_fields.get("status") != UserStatus.ACTIVE:
            raise ValueError("Superuser must have status=ACTIVE")

        return self._create_user(phone_number, password, **extra_fields)
