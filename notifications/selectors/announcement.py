from django.utils import timezone
from django.db.models import Q, QuerySet

from notifications.models import (
    AnnouncementModel,
)
from notifications.repositories import AnnouncementRepository


class AnnouncementSelector:
    @staticmethod
    def get_visible_announcements() -> QuerySet[AnnouncementModel]:
        now = timezone.now()

        return (
            AnnouncementRepository.get_queryset()
            .filter(
                is_active=True,
                starts_at__lte=now,
            )
            .filter(Q(expires_at__isnull=True) | Q(expires_at__gte=now))
            .order_by(
                "-is_pinned",
                "-created_at",
            )
        )
