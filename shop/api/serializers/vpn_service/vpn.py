from rest_framework import serializers

from shop.models import VPNProvisionedServiceModel


class VPNSerializer(serializers.ModelSerializer):
    """
    VPN service serializer.
    """

    class Meta:
        model = VPNProvisionedServiceModel
        fields = (
            "id",
            "subscription_link",
            "content",
            "expires_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = ["__all__"]
