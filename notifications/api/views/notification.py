import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from config.utils import APIResponse
from notifications.selectors import NotificationSelector
from notifications.api.serializers import NotificationListSerializer

logger = logging.getLogger("notifications.notification-list")


class NotificationListAPIView(APIView):
    """
    Retrieve notifications for authenticated user.
    """

    http_method_names = ["get"]

    permission_classes = [IsAuthenticated]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def get(self, request: Request, *args, **kwargs):
        try:
            notifications = NotificationSelector.get_user_notifications(request.user)

            unread_count = NotificationSelector.get_unread_count(request.user)

            serializer = NotificationListSerializer(
                {
                    "notifications": notifications,
                },
                context={
                    "unread_count": unread_count,
                },
            )

            logger.info(
                "Notifications retrieved for user %s",
                request.user.id,
            )

            return APIResponse.success(
                data=serializer.data,
                message="اعلان‌ها با موفقیت دریافت شدند.",
            )

        except Exception:
            logger.exception(
                "Error retrieving notifications for user %s",
                request.user.id,
            )

            return APIResponse.error(
                message="خطا در دریافت اعلان‌ها.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                errors="خطا در دریافت اعلان‌ها.",
            )
