from rest_framework import serializers

from notifications.models import NotificationModel


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationModel
        fields = (
            "id",
            "title",
            "message",
            "notification_type",
            "is_read",
            "created_at",
        )
        read_only_fields = (
            "id",
            "title",
            "message",
            "notification_type",
            "created_at",
        )


class NotificationListSerializer(serializers.Serializer):
    unread_count = serializers.SerializerMethodField()
    notifications = NotificationSerializer(many=True)

    def get_unread_count(self, obj):
        return self.context["unread_count"]
