from django.db import transaction

from accounts.models import UserModel
from notifications.enums import NotificationType
from notifications.models import NotificationModel
from notifications.repositories import NotificationRepository


class NotificationService:
    """Service for notification operations."""

    @staticmethod
    @transaction.atomic
    def create(
        user: UserModel,
        title: str,
        message: str,
        notification_type: NotificationType = NotificationType.INFO,
    ):
        return NotificationRepository.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type,
        )

    @staticmethod
    @transaction.atomic
    def mark_as_read(user: UserModel, notification_id):
        return NotificationRepository.mark_as_read(user, notification_id)

    @staticmethod
    @transaction.atomic
    def mark_all_as_read(user: UserModel):
        return NotificationRepository.mark_all_as_read(user)
