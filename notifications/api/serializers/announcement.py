from rest_framework import serializers

from notifications.models import AnnouncementModel


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementModel
        fields = (
            "id",
            "title",
            "description",
            "type",
            "button_text",
            "button_url",
            "starts_at",
            "expires_at",
            "created_at",
        )
