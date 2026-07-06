from rest_framework import serializers
from commerce.models import V2rayVPNModel
from commerce.services import V2raySubscriptionParser
from django.utils import timezone


class V2rayVPNSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(
        source="order_item.product.title",
        read_only=True,
    )

    product_id = serializers.UUIDField(
        source="order_item.product.id",
        read_only=True,
    )

    plan_id = serializers.UUIDField(
        source="order_item.plan.id",
        read_only=True,
    )

    plan_title = serializers.CharField(
        source="order_item.plan.title",
        read_only=True,
    )

    stats = serializers.SerializerMethodField()

    class Meta:
        model = V2rayVPNModel
        fields = (
            "id",
            "product_id",
            "product_title",
            "plan_id",
            "plan_title",
            "subscription_link",
            "content",
            "expires_at",
            "created_at",
            "stats",
        )
        read_only_fields = fields

    def _get_subscription(self, obj):
        if hasattr(obj, "_cache"):
            return obj._cache

        url = getattr(obj, "subscription_json_link", None)

        if not url:
            obj._cache = V2raySubscriptionParser.fallback()
        else:
            obj._cache = V2raySubscriptionParser.fetch(url)

        return obj._cache

    def get_stats(self, obj):
        data = self._get_subscription(obj)

        expired = obj.expires_at and obj.expires_at <= timezone.now()

        return {
            "remaining_volume": data.get("remaining_volume"),
            "status": "expired" if expired else data.get("status", "unknown"),
        }
