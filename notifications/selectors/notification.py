from notifications.repositories import NotificationRepository


class NotificationSelector:
    @staticmethod
    def get_user_notifications(user):
        return NotificationRepository.get_user_notifications(user)

    @staticmethod
    def get_unread_count(user) -> int:
        return NotificationRepository.get_unread_count(user)
