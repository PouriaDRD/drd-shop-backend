from django.db import transaction
from django.db.models import QuerySet

from accounts.models import UserModel
from notifications.enums import NotificationType
from notifications.models import NotificationModel


class NotificationRepository:
    """Repository for notification operations."""

    @staticmethod
    @transaction.atomic
    def create(
        user: UserModel,
        title: str,
        message: str,
        notification_type: NotificationType = NotificationType.INFO,
    ) -> NotificationModel:
        """Create a new notification."""
        return NotificationModel.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type,
            is_read=False,
        )

    @staticmethod
    def get_user_notifications(user: UserModel):
        return NotificationModel.objects.filter(
            user=user,
        ).order_by("-created_at")

    @staticmethod
    def get_by_id(notification_id):
        try:
            return NotificationModel.objects.get(id=notification_id)
        except NotificationModel.DoesNotExist:
            return None

    @staticmethod
    def get_unread_queryset(user: UserModel):
        return NotificationModel.objects.filter(
            user=user,
            is_read=False,
        )

    @staticmethod
    def get_unread_count(user: UserModel) -> int:
        return NotificationModel.objects.filter(
            user=user,
            is_read=False,
        ).count()

    @staticmethod
    @transaction.atomic
    def mark_as_read(user: UserModel, notification_id):
        notification = NotificationModel.objects.get(id=notification_id, user=user)
        notification.is_read = True
        notification.save(
            update_fields=["is_read"],
        )
        return notification

    @staticmethod
    @transaction.atomic
    def mark_all_as_read(user: UserModel) -> int:
        return NotificationModel.objects.filter(
            user=user,
            is_read=False,
        ).update(is_read=True)
