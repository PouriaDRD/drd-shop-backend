import uuid

from django.db import models
from django.utils import timezone
from notifications.enums import NotificationType


class AnnouncementModel(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=200)

    description = models.TextField()

    type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.INFO,
    )

    is_active = models.BooleanField(default=True)

    is_pinned = models.BooleanField(default=False)

    button_text = models.CharField(max_length=50, blank=True)

    button_url = models.URLField(blank=True)

    starts_at = models.DateTimeField(default=timezone.now)

    expires_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "announcements"

        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"

        ordering = ["-is_pinned", "-created_at"]

    def __str__(self):
        return self.title

    @property
    def is_visible(self):
        now = timezone.now()

        if not self.is_active:
            return False

        if self.starts_at > now:
            return False

        if self.expires_at and self.expires_at < now:
            return False

        return True
