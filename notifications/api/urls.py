from django.urls import path

from notifications.api.views import (
    AnnouncementListAPIView,
    NotificationListAPIView,
)

urlpatterns = [
    path("", NotificationListAPIView.as_view(), name="notifications"),
    path("announcements/", AnnouncementListAPIView.as_view(), name="announcements"),
]
