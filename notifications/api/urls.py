from django.urls import path

from notifications.api.views import (
    AnnouncementListAPIView,
    NotificationListAPIView,
)

urlpatterns = [
    path("announcements/", AnnouncementListAPIView.as_view(), name="announcements"),
    path("notifications/", NotificationListAPIView.as_view(), name="notifications"),
]
