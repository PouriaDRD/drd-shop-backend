from django.db import transaction

from accounts.models import UserModel
from accounts.repositories import UserRepository

from notifications.enums import NotificationType
from notifications.models import NotificationModel
from notifications.repositories import NotificationRepository


class NotificationService:
    """Service for notification operations."""

    @staticmethod
    @transaction.atomic
    def create_success(
        user: UserModel,
        title: str,
        message: str,
    ):
        return NotificationRepository.create(
            user=user,
            title=title,
            message=message,
            notification_type=NotificationType.INFO,
        )

    @staticmethod
    @transaction.atomic
    def create_error(email: str, title: str, message: str):
        user = UserRepository.get_by_email(email)
        if not user:
            return

        return NotificationRepository.create(
            user=user,
            title=title,
            message=message,
            notification_type=NotificationType.ERROR,
        )

    @staticmethod
    @transaction.atomic
    def create_warning(email: str, title: str, message: str):
        user = UserRepository.get_by_email(email)
        if not user:
            return

        return NotificationRepository.create(
            user=user,
            title=title,
            message=message,
            notification_type=NotificationType.WARNING,
        )

    @staticmethod
    @transaction.atomic
    def mark_as_read(user: UserModel, notification_id):
        return NotificationRepository.mark_as_read(user, notification_id)

    @staticmethod
    @transaction.atomic
    def mark_all_as_read(user: UserModel):
        return NotificationRepository.mark_all_as_read(user)
