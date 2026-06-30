from django.db.models import QuerySet

from notifications.models import AnnouncementModel


class AnnouncementRepository:
    @staticmethod
    def get_queryset() -> QuerySet[AnnouncementModel]:
        return AnnouncementModel.objects.all()
