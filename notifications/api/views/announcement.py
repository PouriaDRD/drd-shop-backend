import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle

from config.utils import APIResponse

from notifications.selectors import AnnouncementSelector
from notifications.api.serializers import AnnouncementSerializer

logger = logging.getLogger("notifications.announcement-list")


class AnnouncementListAPIView(APIView):
    """
    Retrieve active announcements.
    """

    http_method_names = ["get"]

    permission_classes = [AllowAny]

    throttle_scope = "anon"
    throttle_classes = [ScopedRateThrottle]

    def get(self, request: Request, *args, **kwargs):
        try:

            announcements = AnnouncementSelector.get_visible_announcements()

            serializer = AnnouncementSerializer(
                announcements,
                many=True,
            )

            logger.info("Announcements retrieved")

            return APIResponse.success(
                data=serializer.data,
                message="اعلامیه‌ها با موفقیت دریافت شدند.",
            )

        except Exception:
            logger.exception(
                "Error retrieving announcements",
            )

            return APIResponse.error(
                message="خطا در دریافت اعلامیه‌ها.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
