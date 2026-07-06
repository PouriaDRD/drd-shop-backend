import logging

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from config.utils import APIResponse
from notifications.services import NotificationService
from notifications.selectors import NotificationSelector
from notifications.api.serializers import NotificationListSerializer

logger = logging.getLogger("notifications.notification-list")


class NotificationListAPIView(ListAPIView):
    """
    Retrieve notifications for authenticated user.
    """

    http_method_names = ["get"]

    permission_classes = [IsAuthenticated]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    serializer_class = NotificationListSerializer

    def get_queryset(self):  # type: ignore
        return NotificationSelector.get_user_notifications(self.request.user)

    def list(self, request: Request, *args, **kwargs):
        try:
            notifications = self.get_queryset()

            unread_count = NotificationSelector.get_unread_count(request.user)

            serializer = NotificationListSerializer(
                {
                    "notifications": notifications,
                },
                context={
                    "unread_count": unread_count,
                },
            )

            logger.info(f"Notifications retrieved for user {request.user}")

            return APIResponse.success(
                data=serializer.data,
                message="اعلان‌ها با موفقیت دریافت شدند.",
            )

        except Exception as e:
            logger.exception(f"Error retrieving notifications for user {e}")

            return APIResponse.error(
                message="خطا در دریافت اعلان‌ها.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class NotificationMarkAsReadAPIView(APIView):
    """
    Mark a notification as read.
    """

    http_method_names = ["patch"]

    permission_classes = [IsAuthenticated]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def patch(self, request: Request, *args, **kwargs):
        try:
            user = request.user
            notification_id = kwargs["notification_id"]

            notification = NotificationService.mark_as_read(user, notification_id)

            logger.info(f"Notification marked as read: {str(notification.id)}")
            return APIResponse.success(
                data={
                    "is_read": True,
                },
                message="اعلان با موفقیت خوانده شد.",
                status_code=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"Error marking notification as read: {e}")
            return APIResponse.error(
                message="خطا در خواندن اعلان.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class NotificationMarkAllAsReadAPIView(APIView):
    """
    Mark all notifications as read.
    """

    http_method_names = ["post"]

    permission_classes = [IsAuthenticated]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request, *args, **kwargs):
        try:
            user = request.user

            notifications = NotificationService.mark_all_as_read(user)
            logger.info(f"Notifications marked as read: {str(notifications)}")

            return APIResponse.success(
                data={
                    "is_read": True,
                },
                message="اعلان‌ها با موفقیت خوانده شدند.",
                status_code=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"Error marking all notifications as read: {e}")
            return APIResponse.error(
                message="خطا در خواندن اعلان‌ها.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
