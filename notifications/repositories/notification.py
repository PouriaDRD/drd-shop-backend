from django.db.models import QuerySet

from notifications.models import NotificationModel


class NotificationRepository:
    @staticmethod
    def get_user_notifications(user):
        return NotificationModel.objects.filter(
            user=user,
        ).order_by("-created_at")

    @staticmethod
    def get_unread_queryset(user):
        return NotificationModel.objects.filter(
            user=user,
            is_read=False,
        )

    @staticmethod
    def get_unread_count(user) -> int:
        return NotificationModel.objects.filter(
            user=user,
            is_read=False,
        ).count()

    @staticmethod
    def mark_as_read(notification: NotificationModel):
        notification.is_read = True
        notification.save(update_fields=["is_read"])
        return notification

    @staticmethod
    def mark_all_as_read(user) -> int:
        return NotificationModel.objects.filter(
            user=user,
            is_read=False,
        ).update(is_read=True)
