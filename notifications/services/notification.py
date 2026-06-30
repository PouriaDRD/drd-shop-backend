from notifications.models import NotificationModel
from notifications.repositories import NotificationRepository


class NotificationService:
    @staticmethod
    def mark_as_read(notification: NotificationModel):
        return NotificationRepository.mark_as_read(notification)

    @staticmethod
    def mark_all_as_read(user):
        return NotificationRepository.mark_all_as_read(user)
