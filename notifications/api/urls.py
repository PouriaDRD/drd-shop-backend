from django.urls import path

from notifications.api.views import (
    AnnouncementListAPIView,
    NotificationListAPIView,
    NotificationMarkAsReadAPIView,
    NotificationMarkAllAsReadAPIView,
)

urlpatterns = [
    path("", NotificationListAPIView.as_view(), name="notifications"),
    path("announcements/", AnnouncementListAPIView.as_view(), name="announcements"),
    path(
        "notifications/<int:notification_id>/",
        NotificationMarkAsReadAPIView.as_view(),
        name="notification-mark-as-read",
    ),
    path(
        "notifications/mark-all-as-read/",
        NotificationMarkAllAsReadAPIView.as_view(),
        name="notification-mark-all-as-read",
    ),
]
