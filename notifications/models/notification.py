import uuid
from django.db import models
from django.conf import settings

from notifications.enums import NotificationType


class NotificationModel(models.Model):
    """A notification message sent to a specific user."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        help_text="The recipient of the notification.",
    )

    title = models.CharField(max_length=255)
    message = models.TextField()

    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.INFO,
    )

    is_read = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title} ({self.user})"

    class Meta:
        db_table = "notifications"

        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

        ordering = ("-created_at",)
