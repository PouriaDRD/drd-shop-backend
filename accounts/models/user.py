import uuid
from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .user_manager import UserManager
from accounts.enums import UserRole, UserStatus
from accounts.utils import normalize_iranian_mobile, validate_iranian_mobile


class UserModel(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model using phone number authentication.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    phone_number = models.CharField(
        max_length=11,
        unique=True,
        db_index=True,
        validators=[validate_iranian_mobile],
    )

    email = models.EmailField(
        unique=True,
        null=True,
        blank=True,
        validators=[
            EmailValidator(
                message="Enter a valid email address.",
                code="invalid_email",
            )
        ],
        help_text="Enter a valid email address.",
    )

    status = models.CharField(
        max_length=20,
        choices=UserStatus.choices,
        default=UserStatus.ACTIVE,
        db_index=True,
    )

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER,
        db_index=True,
    )

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Custom manager
    objects = UserManager()

    # Authentication field
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    # Permissions
    @property
    def is_active(self):  # type: ignore
        return self.status == UserStatus.ACTIVE

    @property
    def is_staff(self):
        return self.is_superuser or self.role == UserRole.ADMIN

    @property
    def is_superuser(self):
        return self.role == UserRole.SUPERUSER

    def __str__(self) -> str:
        """
        String representation of user.
        """

        return str(self.phone_number or self.email or self.id)

    class Meta:
        """
        Database metadata for UserModel.
        """

        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("-created_at",)

    def clean(self):
        """
        Normalize data before validation.
        """

        # Normalize phone number before saving
        self.phone_number = normalize_iranian_mobile(self.phone_number)

        super().clean()

    def save(self, *args, **kwargs):
        """
        Ensure full validation before saving.
        """

        self.full_clean()
        return super().save(*args, **kwargs)
